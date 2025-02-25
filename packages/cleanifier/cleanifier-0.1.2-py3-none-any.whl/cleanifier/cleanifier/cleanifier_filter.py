"""
cleanifier_classify:
Removing contaminations.
by Jens Zentgraf & Sven Rahmann, 2019--2023
"""

import datetime
from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor, as_completed
from math import ceil
from pathlib import Path


import numpy as np
from numba import njit, uint32, uint64
from ..io.hashio import load_hash
from ..kmers import compile_kmer_processor, compile_positional_kmer_processor
from ..io.generalio import InputFileHandler, OutputFileHandler
from ..io.fastqio import fastq_chunks, fastq_chunks_paired
from ..lowlevel.bitarray import bitarray
from ..dnaencode import (
    quick_dna_to_2bits,
    twobits_to_dna_inplace,
    compile_twobit_to_codes)
from ..lowlevel import debug
from ..mask import create_mask


def compile_coverage_based_classification(cov, mask, threshold):
    popcount = cov.popcount

    @njit(nogil=True)
    def classify_coverage(counts, coverage_vector, size):
        ret_keep = 0
        ret_filter = 1

        # number of bases covered by k-mers
        n_covered_bases = popcount(coverage_vector)

        if n_covered_bases == 0:
            assert counts[0] == 0
            return ret_keep

        if n_covered_bases / size >= threshold:
            return ret_filter

        return ret_keep

    return classify_coverage


def compile_get_kmer_values(mask, rcmode, h, prefetch_level, count=True, ba=None):
    # tmask: mask in tuple form
    get_bf1, get_bf2, get_bf3 = h.private.get_bf
    prefetch = h.private.prefetch_bucket
    get_subtable_subkey = h.private.get_subtable_subkey_from_key
    get_value_from_subtable_subkey = h.private.get_value_from_st_sk

    k = mask.k
    W = mask.w

    tmask = mask.tuple

    # If we use a covarge based approach we have to translate the mask to a uint64
    if count is False or ba is not None:
        assert count is False
        assert ba is not None
        mask = 0
        for i in tmask:
            mask += 2**i
        mask = uint64(mask)
        set_value_at = ba.set

    @njit(nogil=True,
        locals=dict(code=uint64, subkey=uint64, subtable=uint64, value=uint64))
    def count_values(ht, code, count):
        subtable, subkey = get_subtable_subkey(code)
        if prefetch_level == 1:
            prefetch(ht, subtable, get_bf2(subkey)[0])
        if prefetch_level == 2:
            prefetch(ht, subtable, get_bf2(subkey)[0])
            prefetch(ht, subtable, get_bf3(subkey)[0])
            # 1: value NOT found, 0 value found
        notfound = get_value_from_subtable_subkey(ht, subtable, subkey)
        if not notfound:
            count[0] += 1
        return False

    @njit(nogil=True, locals=dict())
    def get_coverage(ht, code, pos, cov):
        counts = cov[0]
        cov = cov[1]
        subtable, subkey = get_subtable_subkey(code)
        if prefetch_level == 1:
            prefetch(ht, subtable, get_bf2(subkey)[0])
        if prefetch_level == 2:
            prefetch(ht, subtable, get_bf2(subkey)[0])
            prefetch(ht, subtable, get_bf3(subkey)[0])
        # 1: value NOT found, 0 value found
        notfound = get_value_from_subtable_subkey(ht, subtable, subkey, default=1)
        if not notfound:
            set_value_at(cov, pos, mask, W)
            cov[0] += 1
        return False  # we never fail!

    # because the supplied function 'count_values' has ONE extra parameter (counts),
    # the generated function process_kmers also gets ONE extra parameter (counts)!
    if count:
        k, process_kmers = compile_kmer_processor(tmask, count_values, rcmode=rcmode)
    else:
        k, process_kmers = compile_positional_kmer_processor(tmask, get_coverage, rcmode=rcmode)

    @njit(nogil=True)
    def classify_read(ht, seq, values):
        process_kmers(ht, seq, 0, len(seq), values)

    return classify_read


def compile_classify_read_from_fastq(
        mode, mask, rcmode, path, h, threads, pairs, threshold,
        bufsize=2**23, chunkreads=(2**23) // 200,
        filt=False, count=False, prefetchlevel=0,
        compression="gz", show_progress=False):

    if compression != "none":
        compression = "." + compression
    else:
        compression = ""

    bitarrays = [None] * threads
    ba = None

    if mode == "coverage":
        debugprint0("- using coverage based mode")
        count_kmers = False
        # The bitarray is created to get the set and get functions.
        # The array itself is not used
        ba = bitarray(200)
        # These bit arrays are used
        bitarrays = list(np.zeros(30, dtype=np.uint64) for i in range(threads))
        classify = compile_coverage_based_classification(ba, mask, threshold)
    elif mode == "quick":
        count_kmers = True
    else:
        raise ValueError(f"Unknown mode '{mode}'")

    get_kmer_values = compile_get_kmer_values(mask, rcmode, h, prefetchlevel, count_kmers, ba)
    _, twobit_to_code = compile_twobit_to_codes(mask, rcmode)

    get_value = h.get_value
    k = mask.k
    w = mask.w

    @njit(nogil=True, locals=dict(
        third_kmer=uint64, third=uint64,
        thirdlast_kmer=uint64, thirdlast=uint64))
    def get_classification(ht, sq):
        # quick classification mode for a single end read
        # get 2 k-mers (3rd and 3rd-last)
        third_kmer = twobit_to_code(sq, 2)
        thirdlast_kmer = twobit_to_code(sq, len(sq) - w - 2)
        # look up values of both k-mers, ignore weak status (good thing?!)
        third = get_value(ht, third_kmer, default=1)
        thirdlast = get_value(ht, thirdlast_kmer, default=1)
        if third and thirdlast:
            return 0  # keep
        return 1

    @njit(nogil=True, locals=dict(
        third_kmer1=uint64, third_sq1=uint64,
        third_kmer2=uint64, third_sq2=uint64,
        thirdlast_kmer1=uint64, thirdlast_sq1=uint64,
        thirdlast_kmer2=uint64, thirdlast_sq2=uint64))
    def get_paired_classification(ht, sq1, sq2):
        # quick classification mode for paired end reads
        # get 4 k-mers (3rd and 3rd-last of both sequences)
        third_kmer1 = twobit_to_code(sq1, 2)
        thirdlast_kmer1 = twobit_to_code(sq1, len(sq1) - w - 2)
        third_kmer2 = twobit_to_code(sq2, 2)
        thirdlast_kmer2 = twobit_to_code(sq2, len(sq2) - w - 2)
        # look up values of all 4 k-mers, ignore weak status (good thing?!)
        third_sq1 = get_value(ht, third_kmer1, default=1)
        thirdlast_sq1 = get_value(ht, thirdlast_kmer1, default=1)
        third_sq2 = get_value(ht, third_kmer2, default=1)
        thirdlast_sq2 = get_value(ht, thirdlast_kmer2, default=1)
        if third_sq1 and thirdlast_sq1 and third_sq2 and thirdlast_sq2:
            return 0
        return 1

    @njit(nogil=True)
    def classify_kmers_chunkwise(threadid, buf, linemarks, ht,
         covered_bases=None):

        n = linemarks.shape[0]
        classifications = np.zeros(n, dtype=np.uint8)
        counts = np.zeros(8, dtype=np.uint32)
        for i in range(n):

            # get sequence
            sq = buf[linemarks[i, 0]:linemarks[i, 1]]

             # tranlate seuqences to two bit encoding
            quick_dna_to_2bits(sq)

            if mode == "quick":
                classifications[i] = get_classification(ht, sq)
            else:
                # check if bitarray is big enough for the sequence
                seq_size = int(ceil(len(sq) / 64))
                if seq_size > covered_bases.size:
                    debugprint1("# increase array size to", seq_size, "sequence length=", len(sq))
                    # increase size buffer 1
                    covered_bases = np.zeros(seq_size, dtype=uint64)
                counts[:] = 0
                # rest all bitarrays
                covered_bases.fill(0)
                # get values for each k-mer
                get_kmer_values(ht, sq, (counts, covered_bases))

                # classify the read based on the values
                classifications[i] = classify(counts, covered_bases, len(sq))

            # translate the two bit encoding back
            twobits_to_dna_inplace(buf, linemarks[i, 0], linemarks[i, 1])

        return threadid, (classifications, linemarks)

    @njit(nogil=True)
    def classify_paired_kmers_chunkwise(threadid, buf, linemarks, buf1, linemarks1, ht,
         covered_bases=None):
        n = linemarks.shape[0]
        classifications = np.zeros(n, dtype=np.uint8)
        counts = np.zeros(8, dtype=np.uint32)
        for i in range(n):
            # get both sequences
            sq1 = buf[linemarks[i, 0]:linemarks[i, 1]]
            sq2 = buf1[linemarks1[i, 0]:linemarks1[i, 1]]

            # check if bitarrays are big enough for both sequences
            seq1_size = int(ceil(len(sq1) / 64))
            seq2_size = int(ceil(len(sq2) / 64))

            # tranlate seuqences to two bit encoding
            quick_dna_to_2bits(sq1)
            quick_dna_to_2bits(sq2)

            if mode == "quick":
                classifications[i] = get_paired_classification(ht, sq1, sq2)
            else:
                if seq1_size + seq2_size > covered_bases.size:
                    debugprint1("# increase array size to", seq1_size + seq2_size)
                    # increase size buffer 1
                    covered_bases = np.zeros(seq1_size + seq2_size, dtype=uint64)
                counts[:] = 0
                # reset bitarray
                covered_bases.fill(0)

                # get values for each k-mer
                get_kmer_values(ht, sq1, (counts, covered_bases))

                get_kmer_values(ht, sq2, (counts, covered_bases[seq1_size:]))

                # classify the read based on the values
                classifications[i] = classify(counts, covered_bases, len(sq1) + len(sq2))

            # translate the two bit encoding back
            twobits_to_dna_inplace(buf, linemarks[i, 0], linemarks[i, 1])
            twobits_to_dna_inplace(buf1, linemarks1[i, 0], linemarks1[i, 1])

        return threadid, (classifications, linemarks, linemarks1)

    @njit(nogil=True)
    def get_borders(linemarks, threads):
        n = linemarks.shape[0]
        perthread = (n + (threads - 1)) // threads
        borders = np.empty(threads + 1, dtype=uint32)
        for i in range(threads):
            borders[i] = min(i * perthread, n)
        borders[threads] = n
        return borders

    class DummyContextMgr():
        """a context manager that does nothing at all"""
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def write(*_):
            pass

        def flush(*_):
            pass

    @contextmanager
    def cond_contextmgr(name, suffix, count, filt):
        if count and filt:
            raise ValueError("ERROR: cannot use both --count and --filter option at the same time.")
        if count:
            yield DummyContextMgr()
        elif filt:
            if "filtered" in suffix:
                with OutputFileHandler(name + suffix) as outfile:
                    yield outfile.file
            else:
                yield DummyContextMgr()
        else:
            with OutputFileHandler(name + suffix) as outfile:
                yield outfile.file

    def classify_read_from_fastq_paired(fastqs, pairs, ht):
        counts = [0, 0]
        nprocessed = 0
        with cond_contextmgr(path, f"_filtered.1.fq{compression}", count, filt) as filtered1, \
             cond_contextmgr(path, f"_filtered.2.fq{compression}", count, filt) as filtered2, \
             cond_contextmgr(path, f"_removed.1.fq{compression}", count, filt) as removed1, \
             cond_contextmgr(path, f"_removed.2.fq{compression}", count, filt) as removed2:
            streams = ((filtered1, filtered2), (removed1, removed2))

            with ThreadPoolExecutor(max_workers=threads) as executor:
                for fastq1, fastq2 in zip(fastqs, pairs):
                    with InputFileHandler(fastq1) as fq, \
                         InputFileHandler(fastq2) as fp:
                        for chunk in fastq_chunks_paired((fq, fp), bufsize=bufsize * threads, maxreads=chunkreads * threads):
                            if show_progress:
                                debugprint0(f"Processed {nprocessed} reads", end="\r")
                            # c0 buffer of first fastq file
                            # c1 linemarks for the first fastq file
                            # c2 buffer of the second fastq file
                            # c3 linemarks of the second fastq file
                            c0, c1, c2, c3 = chunk
                            borders = get_borders(c1, threads)  # the number of sequences in c1 and c3 is equal
                            futures = [executor.submit(
                                classify_paired_kmers_chunkwise, i, c0, c1[borders[i]:borders[i + 1]],
                                c2, c3[borders[i]:borders[i + 1]], ht,
                                bitarrays[i])
                                for i in range(threads)]
                            for fut in as_completed(futures):
                                threadid, (classifications, linemarks, linemarks2) = fut.result()
                                start_write = datetime.datetime.now()
                                if count:
                                    for seq in range(linemarks.shape[0]):
                                        cl = classifications[seq]
                                        counts[cl] += 1
                                elif filt:
                                    for seq in range(linemarks.shape[0]):
                                        cl = classifications[seq]
                                        counts[cl] += 1
                                        if cl == 0:
                                            lms1, lms2 = linemarks[seq], linemarks2[seq]
                                            streams[cl][0].write(c0[lms1[2]:lms1[3]])
                                            streams[cl][1].write(c2[lms2[2]:lms2[3]])
                                else:
                                    for seq in range(linemarks.shape[0]):
                                        cl = classifications[seq]
                                        counts[cl] += 1
                                        lms1, lms2 = linemarks[seq], linemarks2[seq]
                                        streams[cl][0].write(c0[lms1[2]:lms1[3]])
                                        streams[cl][1].write(c2[lms2[2]:lms2[3]])
                            nprocessed += len(c1)
                    # all chunks processed
            if show_progress:
                debugprint0(f"Processed {nprocessed} reads")
            # ThreadPool closed
            for s in streams:
                s[0].flush()
                s[1].flush()
            return counts

    def classify_read_from_fastq_single(fastqs, ht):
        counts = [0, 0]  # keep, filter
        nprocessed = 0
        with cond_contextmgr(path, f"_filtered.fq{compression}", count, filt) as filtered, \
             cond_contextmgr(path, f"_remove.fq{compression}", count, filt) as remove:
            streams = (filtered, remove)
            running_jobs = []
            with ThreadPoolExecutor(max_workers=threads) as executor:
                for fastq in fastqs:
                    with InputFileHandler(fastq) as fq:
                        for chunk in fastq_chunks(fq, bufsize=bufsize * threads, maxreads=chunkreads * threads):
                            if show_progress:
                                debugprint0(f"Processed {nprocessed} reads of {fastq}", end="\r")
                            # c0 = buffer
                            # c1 = linemarks
                            c0, c1 = chunk
                            borders = get_borders(c1, threads)

                            futures = [executor.submit(
                                classify_kmers_chunkwise, i, c0, c1[borders[i]:borders[i + 1]], ht,
                                bitarrays[i])
                                for i in range(threads)]
                            for fut in as_completed(futures):
                                threadid, (classifications, linemarks) = fut.result()
                                if count:
                                    for seq in range(linemarks.shape[0]):
                                        cl = classifications[seq]
                                        counts[cl] += 1
                                elif filt:
                                    for seq in range(linemarks.shape[0]):
                                        cl = classifications[seq]
                                        counts[cl] += 1
                                        if cl == 0:
                                            lms = linemarks[seq]
                                            streams[cl].write(c0[lms[2]:lms[3]])
                                else:
                                    for seq in range(linemarks.shape[0]):
                                        cl = classifications[seq]
                                        counts[cl] += 1
                                        lms = linemarks[seq]
                                        streams[cl].write(c0[lms[2]:lms[3]])

                            nprocessed += len(c1)
                # all chunks processed
            # ThreadPool closed
            if show_progress:
                debugprint0(f"Processed {nprocessed} reads of {fastq}")
            for s in streams:
                s.flush()
        return counts

    classify_read_from_fastq = (
        classify_read_from_fastq_paired if pairs
        else classify_read_from_fastq_single)
    return classify_read_from_fastq


def print_class_stats(prefix, stats):
    classes = ["keep", "filter"]

    percentages = [i / sum(stats) * 100 for i in stats]
    str_counts = "\t".join(str(i) for i in stats)
    ndigits = max(map(lambda x: len(str(x)), stats))

    print("\n## Classification Statistics")
    print("\n```")
    print("prefix\tkeep\tfilter")
    print(f"{prefix}\t{str_counts}")
    print("```\n")
    print("```")
    print(f"| prefix    | {prefix} ")
    for i in range(len(classes)):
        print(f"| {classes[i]:9s} | {stats[i]:{ndigits}d} | {percentages[i]:5.2f}% |")
    print("```")
    print()


def main(args):
    """main method for classifying reads"""
    global debugprint0, debugprint1, debugprint2
    global timestamp0, timestamp1, timestamp2
    debugprint0, debugprint1, debugprint2 = debug.debugprint
    timestamp0, timestamp1, timestamp2 = debug.timestamp

    starttime = timestamp0(msg="\n# Cleanifier filter")
    debugprint0("\n- (c) 2019-2023 by Sven Rahmann, Jens Zentgraf, Algorithmic Bioinformatics, Saarland University")
    debugprint0("- Licensed under the MIT License")

    if 0 > args.threshold > 1:
        debugprint0(f"- {args.threshold} is not a valid threshold. 0.0 < t < 1.0")
        exit(1)

    # Load hash table (index)
    h, values, infotup = load_hash(args.index, shared_memory=args.shared)
    (hashinfo, valueinfo, optinfo, appinfo) = infotup
    bits = values.bits
    mask = create_mask(appinfo['mask'])
    k, tmask = mask.k, mask.tuple
    assert k == appinfo['k']
    rcmode = appinfo.get('rcmode', values.RCMODE)
    if rcmode is None:
        rcmode = values.RCMODE
    if not isinstance(rcmode, str):
        rcmode = rcmode.decode("ASCII")
    chunksize = int(args.chunksize * 2**20)
    chunkreads = args.chunkreads or (chunksize // 200)

    # classify reads from either FASTQ or FASTA files
    timestamp1(msg='- Begin classification')
    debugprint1(f"- mask: {k=}, w={tmask[-1]+1}, tuple={tmask}")

    mode = args.mode

    if not args.fastq:
        # NO --fastq given, nothing to do
        debugprint0("- No FASTQ files to classify. Nothing to do. Have a good day.")
        exit(1)

    # check if same number of fastq files are provided for paired end reads
    paired = False
    if args.pairs:
        if len(args.fastq) != len(args.pairs):
            raise ValueError("- Different number of files in --fastq and --pairs")
        paired = True

    if args.prefix is None:
        if len(args.fastq) > 1:
            raise ValueError("- Please provide an output name using --out or -o")
        args.prefix = Path(args.fastq[0]).stem
        if args.prefix.endswith(("fq", "fastq")):
            args.prefix = Path(args.prefix).stem

    if args.prefix.endswith("/"):
        fastqname = Path(args.fastq[0]).stem
        if fastqname.endswith(("fq", "fastq")):
            args.prefix = args.prefix + Path(fastqname).stem
        if len(args.fastq) > 1:
            debugprint0("- Warning: No output file name specified.")
            debugprint0(f"  The output will be saved in {args.prefix}")

    if args.count and args.filter:
        args.filter = False

    # compile classification method
    classify_read_from_fastq = compile_classify_read_from_fastq(
        mode, mask, rcmode,
        args.prefix, h, args.threads, paired, args.threshold,
        bufsize=chunksize, chunkreads=chunkreads,
        filt=args.filter, count=args.count, prefetchlevel=args.prefetchlevel,
        compression=args.compression, show_progress=args.progress)

    if paired:
        counts = classify_read_from_fastq(args.fastq, args.pairs, h.hashtable)
    else:
        counts = classify_read_from_fastq(args.fastq, h.hashtable)
    print_class_stats(args.prefix, counts)

    debugprint0("## Running time statistics\n")
    timestamp0(starttime, msg="- Running time")
    timestamp0(starttime, msg="- Running time", minutes=True)
    timestamp0(msg="- Done.")
