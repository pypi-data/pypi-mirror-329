# cleanifier: Fast lightweight accurate contamination removal

This tool, cleanifier, uses 3-way bucketed Cuckoo hashing to efficiently remove contamination of a species from samples.


In case of problems file an issue in the issue tracker.

See CHANGELOG.md for recent changes.
Thank you!


----


# Usage Guide

cleanifier is a multi-command tool with several subcommands (like git), in particular
- `cleanifier index` builds an index (a bucketed 3-way Cuckoo hash table)
- `cleanifier filter` cleans a sequences sample (FASTQ files) using an existing index

It is a good idea to run `cleanifier index --help` to see all available options.
Using `--help` works on any subcommand.

### Prebuild index
We provide an index to filter human data.
The index contains all $k$-mers of the t2t-reference genome, and in addition, all variants, reported by the 1k genome project, that have an allel frequency of at least `0.01`.
The index can be downloaded [here](https://kingsx.cs.uni-saarland.de/index.php/s/9oTeKTobKE4fKgg).

### How to build an index

To build an index for cleanifier, several parameters must be provided, which are described in the following.

First, a file name and a path for the index must be chosen.
The index is stored in two files. We will use `myindex` to store the index in the current folder.

Second, all reference genomes that should be removed must be provided (in FASTA files).
These files can be provided as an uncompressed file or compressed using `gzip`, `bzip2` or `xz`.
The corresponding option is `--files`.
Each option can take several arguments as files. 
```
cleanifier index --index myindex --files ref1.fa.gq [ref2.fa.gz ...]
```

We must specify the size of the hash table:

- `-n` or  `--nobjects`: number of k-mers that will be stored in the hash table. This depends on the used reference genomes and must be estimated beforehand! As a precise estimate of the number of different k-mers can be difficult, you can err on the safe side and provide a generously large estimate, examine the final (low) load factor and then rebuild the index with a smaller `-n` parameter to achieve the desired load. There are also some tools that quickly estimate the number of distinct k-mers in large files, such as [ntCard](https://github.com/bcgsc/ntCard) or [KmerEstimate](https://github.com/srbehera11/KmerEstimate). As a guide: The Human genome consists of roughly 2.5 billion 25-mers.
**This option must be specified; there is no default!**


We may further specify additional properties of the hash table:

- `-b` or `--bucketsize` indicates how many elements can be stored in one bucket (or page). This is 4 by default.

- `--fill` between 0.0 and 1.0 describes the desired fill rate or load factor of the hash table.
Together with `-n`, the number of slots in the table is calculated as `ceil(n/fill)`. In our experiments we used 0.88. (The number of buckets is then the smallest odd integer that is at least `ceil(ceil(n/fill)/p)`.)

- `--aligned` or `--unaligned`: indicates whether each bucket should consume a number of bits that is a power of 2. Using `--aligned` ensures that each bucket stays within the same cache line, but may waste space (padding bits), yielding faster speed but possibly (much!) larger space requirements. With `--unaligned`, no bits are used for padding and buckets may cross cache line boundaries. This is slightly slower, but may save a little or a lot of space (depending on the bucket size in bits). The default is `--unaligned`, because the speed decrease is small and the memory savings can be significant.

- `--hashfunctions` defines the parameters for the hash functions used to store the key-value pairs. If the parameter is unspecified, different random functions are chosen each time. The hash functions can be specified using a colon separated list: `--hashfunctions linear945:linear9123641:linear349341847`. It is recommended to have them chosen randomly unless you need strictly reproducible behavior, in which case the example given here is recommended.

The final important parameter is about parallelization:

Most of the parameters can also be provided in a config file (`.yaml`):
- `--cfg` or `--config` defines the path the the config file.
 
### How to classify

To clean a FASTQ sample (one or several single-end or paired-end files), make sure you are in an environment where cleanifier and its dependencies are installed.
Then run the `cleanifier filter` command with a previously built index, such as
```
cleanifier filter --index myindex --fastq single.fq.gz --prefix myresults --mode coverage
```
for single-end reads, or 
```
cleanifier filter --index myindex --fastq paired.1.fq.gz --pairs paired.2.fq.gz --prefix myresults --mode coverage
```
for paired-end reads.

The most important parameter is `--threshold` which defines at which point a read should be filtered out.
The filtering depends on the number of bases that are covered by a $k$-mer that is contained in the original set.
This means, that given a read length of 100 and a $k$-mer size of $k=25$ we should at least pick a threshold of `0.25`. This sorts out a read that already contains a single 25-mer. This also applies to a threshold `<0.25` as 25 bases are always covered by a 25-mer.
For a strict filtering, this can work, but there is a probability that sequencing errors change a $k$-mer in the read to a $k$-mer in the set. If we pick a threshold slightly bigger than the minimum (`0.25`), we need at least 2 or more $k$-mers to be included in the index.

The parameter `--prefix` or equivalently `--out` is required and defines the prefix for all output files; this can be a combination of path and file prefix, such as `/path/to/sorted/samplename`.
The compression type can be specified using the `--compression` parameter.
Currently we support `gz` (default), `bzip`, `xz` and `none` (uncompressed).

Further parameters and options are:
- `-T` defines how many threads are used for classification (4 to 8 is recommended).
