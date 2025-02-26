# cvmcgmlst
![PYPI](https://img.shields.io/pypi/v/cvmcgmlst)
![Static Badge](https://img.shields.io/badge/OS-_Windows_%7C_Mac_%7C_Linux-steelblue)

cvmcgmlst is a tool developed based on the [cvmmlst](https://github.com/hbucqp/cvmmlst) for core genome MLST analysis .

```shell
Usage: cvmcgmlst -i <genome assemble directory> -o <output_directory> -db database_name

Author: Qingpo Cui(SZQ Lab, China Agricultural University)

options:
  -h, --help            show this help message and exit
  -i I                  <input_file>: the PATH of assembled genome file
  -db DB                <database_path>: name of cgMLST database
  -o O                  <output_directory>: output PATH
  -minid MINID          <minimum threshold of identity>, default=95
  -mincov MINCOV        <minimum threshold of coverage>, default=90
  -t T                  <number of threads>: default=8
  -v, --version         Display version

cvmcgmlst subcommand:
  {show_db,init,create_db}
    show_db             <show the list of all available database>
    init                <initialize the reference database>
    create_db           <add custome database, use cvmcgmlst createdb -h for help>
```


## Installation
### Using pip
```shell
pip3 install cvmcgmlst
```

## Dependency
- BLAST+ >2.7.0

**you should add BLAST in your PATH**


## Blast installation
### Windows


Following this tutorial:
[Add blast into your windows PATH](http://82.157.185.121:22300/shares/BevQrP0j8EXn76p7CwfheA)

### Linux/Mac
The easyest way to install blast is:

```
conda install -c bioconda blast
```

## Usage

### 1. Create reference cgmlst database

Users could create their own core genome database. All you need is a FASTA file of nucleotide sequences. The sequence IDs should have the format >locus_allelenumber, where **LOCUS** is the loci name, **ALLELENUMBER** is the number of this allele. 
The curated core genome fasta file should like this:

```shell
>GBAA_RS00015_1
TTGGAAAACATCTCTGATTTATGGAACAGCGCCTTAAAAGAACTCGAAAAAAAGGTCAGT
AAACCAAGTTATGAAACATGGTTAAAATCAACAACCGCACATAATTTAAAGAAAGATGTA
AAGTCAGTTGCCTTTCCTCGCCAAATTGCAATGTATTTGTCACGCGAACTGACAGATTCC
TCCTTACCTAAAATAGGTGAAGAATTTGGTGGACGTGATCATACAACCGTTATCCATGCC
CATGAAAAAATTTCTAAGCTACTTAAGACGGATACGCAATTACAAAAACAAGTTGAAGAA
ATTAACGATATTTTAAAGTAG
>GBAA_RS00015_2
TTGGAAAACATCTCTGATTTATGGAACAGCGCCTTAAAAGAACTCGAAAAAAAGGTCAGT
AAACCAAGTTATGAAACATGGTTAAAATCAACAACCGCACATAATTTAAAGAAAGATGTA
TTAACAATTACGGCTCCAAATGAATTCGCCCGTGATTGGTTAGAATCTCATTATTCAGAG
CTAATTTCGGAAACACTTTATGATTTAACGGGGGCAAAATTAGCTATTCGCTTTATTATT
GCTAAAGCATATAATCCCCTCTTTATTTATGGGGGAGTTGGACTTGGAAAAACCCATTTA
>GBAA_RS00015_3
ATGCTTTATATCGCAAATCAAATCGATTCAAATATTCGTGAACTAGAAGGTGCACTCATC
CGCGTTGTAGCTTATTCATCTTTAATTAACAAGGATATTAATGCTGATTTAGCAGCTGAA
AAAGCTGTTGGAGATGTTTATCAAGTAAAATTAGAAGATTTCAAGGCGAAAAAGCGCACA
AAGTCAGTTGCCTTTCCTCGCCAAATTGCAATGTATTTGTCACGCGAACTGACAGATTCC
CATGAAAAAATTTCTAAGCTACTTAAGACGGATACGCAATTACAAAAACAAGTTGAAGAA
ATTAACGATATTTTAAAGTAG
...
```

After finish installation, you should first initialize the reference database using following command
```shell
cvmcgmlst create_db -file YOUR_REF.fasta -name DBNAME
```
### 2. Show available database

You could list all available databases using the show_db subcommand.
```shell
cvmcgmlst show_db
```
The shell will print available databases
|DB_name|No. of seqs|Update_date|
|---|---|---|
|demo|1|2025-02-25|
|DBNAME|Number of locus|Date|


### Run with your genome
```shell
# Single Genome Mode
cvmcgmlst -i /PATH_TO_ASSEBLED_GENOME/sample.fa -db DBNAME -o PATH_TO_OUTPUT
```




