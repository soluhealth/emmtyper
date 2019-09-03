# emmtyper - Emm Automatic Isolate Labeller

[![CircleCI](https://circleci.com/gh/MDU-PHL/emmtyper.svg?style=svg)](https://circleci.com/gh/MDU-PHL/emmtyper)
[![Coverage Status](https://coveralls.io/repos/github/MDU-PHL/emmtyper/badge.svg?branch=master)](https://coveralls.io/github/MDU-PHL/emmtyper?branch=master) ![PyPI - Implementation](https://img.shields.io/pypi/implementation/emmtyper) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/emmtyper) ![PyPI - Wheel](https://img.shields.io/pypi/wheel/emmtyper) ![Conda](https://img.shields.io/conda/pn/bioconda/emmtyper?label=bioconda) ![GitHub issues](https://img.shields.io/github/issues-raw/MDU-PHL/emmtyper)

## Table of Content

- [emmtyper - Emm Automatic Isolate Labeller](#emmtyper---emm-automatic-isolate-labeller)
  - [Table of Content](#table-of-content)
  - [Background](#background)
    - [Inner workings](#inner-workings)
  - [Requirements](#requirements)
  - [Installation](#installation)
    - [Brew](#brew)
    - [Conda](#conda)
  - [Usage](#usage)
    - [Example Commands](#example-commands)
  - [Result Format](#result-format)
  - [BLAST or PCR?](#blast-or-pcr)
  - [Contact](#contact)

## Background

`emmtyper` is a command line tool for emm-typing of *Streptococcus pyogenes* using a *de novo* or complete assembly.

By default, we use the U.S. Centers for Disease Control and Prevention trimmed emm subtype database,
which can be found [here](https://www2a.cdc.gov/ncidod/biotech/strepblast.asp).
The database is curated by Dr. Velusamy Srinivasan. We take this opportunity to thank Dr. Srinivasan for his work.

### Inner workings

The difficulty in performing M-typing is that there is a single gene of interest (`emm`), but two other homologue genes (`enn` and `mrp`), often referred to as `emm-like`. The homologue genes may or may not occur in the isolate of interest. When performing `emm-typing` from an assembly, we can distinguish betweeen one or more clusters of matches on the contigs. The best match for each of the clusters identified is then parsed from the BLAST results. Where possible, we try to distinguish between matches to the `emm` gene, and matches to one of the `emm-like` genes.

Possible arrangments:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*emm*

---->>>>>>>----

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*mrp*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*emm*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*enn*

---->>>>>>----->>>>>>------>>>>>>-----

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*emm*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*enn*

----->>>>>>------>>>>>>-----

## Requirements

 * `blastn`
 * `ispcr`
 * `python` ≥ 3.6

## Installation

### Brew

```bash
brew install blastn ispcr
pip3 install emmtyper
emmtyper --help
```

### Conda

```bash
conda install -c bioconda emmtyper
```

## Usage

emmtyper has 2 workflows: directly BLASTing the contigs against the DB, or using isPcr to generate an *in silico* PCR product that is then BLASTed against the DB. The BLAST results go through emmtyper's business logic to distinguish between `emm` and `emm-like` alleles and derive the isoolate M-type.

The basic usage of emmtyper is in the form of:

```bash
emmtyper --query contig1 contig2 ... contigN [emmtyper options] <blast|pcr> [workflow options]
```

Select between `<blast|pcr>` to select the desired workflow.

Set global options with `[emmtyper options]`.

These can be inspected with `emmtyper --help`

```bash
optional arguments:
  -h, --help            show this help message and exit
  --query QUERY [QUERY ...]
                        Genome(s) to PCR against. (default: None)
  --db DB               The database to BLAST PCR product against. (default:
                        /path/to/emmtyper/db/emm.fna)
  -v, --version         show program\'s version number and exit
  -save, --save_intermediary
                        Do not remove temporary isPcr and BLAST outputs.
                        (default: False)
  -clust_distance CLUST_DISTANCE
                        Distance in bp between clusters. (default: 500)
  -output_type [{short,verbose,visual}]
                        Choose output type. (default: short)
  -output_file OUTPUT_FILE
                        File to stream final output. (default: stdout)
```

Most of these options are self explanatory. The two expections are:

 1. `clust_distance` defines the minimum distance between clusters of matched sequences on the contigs to generate separate `emm-type` calls for each clusters. Clusters of matches that are within the minimum `clust-distance` are treated as a single location match.
 2. `output_type` demonstrated below.

Set workflow specific options with `[workflow options]`. These vary depending on which workflow is chosen:

You can inspect each with `emmtyper blast --help` or `emmtyper pcr --help`:

For `blast`

```bash
  -h, --help            show this help message and exit
  -dust DUST            Filter query sequence with DUST. Default no.
  -perc_identity PERC_IDENTITY
                        Minimal percent identity of sequence. Default is 95.
  -culling_limit CULLING_LIMIT
                        Total hits to return in a position. Default is 5.
  -mismatch MISMATCH    Threshold for number of mismatch to allow in BLAST
                        hit. Default is 4.
  -align_diff ALIGN_DIFF
                        Threshold for difference between alignment length and
                        subject length in BLAST hit. Default is 5.
  -gap GAP              Threshold gap to allow in BLAST hit. Default is 2.
  --blast_path BLAST_PATH
                        Specify full path to blastn executable. Otherwise
                        search $PATH.
```

For `pcr`:

```bash
  -h, --help            show this help message and exit
  --primer PRIMER       PCR primer. Text file with 3 columns: Name, Forward
                        Primer, Reverse Primer.
  -minPerfect MINPERFECT
                        Minimum size of perfect match at 3\' primer end.
                        Default is 15.
  -minGood MINGOOD      Minimum size where there must be 2 matches for each
                        mismatch. Default is 15; there must be 10 match in
                        15bases primer size.
  -maxSize MAXSIZE      Maximum size of PCR product. Default is 2000.
  -dust DUST            Filter query sequence with DUST. Default no.
  -perc_identity PERC_IDENTITY
                        Minimal percent identity of sequence. Default is 95.
  -culling_limit CULLING_LIMIT
                        Total hits to return in a position. Default is 5.
  -mismatch MISMATCH    Threshold for number of mismatch to allow in BLAST
                        hit. Default is 4.
  -align_diff ALIGN_DIFF
                        Threshold for difference between alignment length and
                        subject length in BLAST hit. Default is 5.
  -gap GAP              Threshold gap to allow in BLAST hit. Default is 2.
  --blast_path BLAST_PATH
                        Specify full path to blastn executable. Otherwise
                        search $PATH.
  --ispacr_path ISPACR_PATH
                        Specify full path to isPcr executable. Otherwise
                        search $PATH.
```

### Example Commands
```bash
emmtyper --query isolate1.fa
emmtyper --query *.fa pcr --primer emmPrimer.tsv
emmtyper --query *.fa -saveIntermediary blast -culling_limit 10 -align_diff 10
emmtyper --query *.fa -output_type visual pcr --primer emmPrimer.tsv -maxSize 2000 -mismatch 5
```

## Result Format
emmtyper has three different result formats: `short`, `verbose`, and `visual`.

emmtyper by default produces the `short` five tab-separated values to the command line. You can call `-output_type <option>` to choose the other two result format.

The short result returns: **Isolate name_Number of clusters_Predicted type_Possible imposters_Answer's EMM cluster**

While the verbose result returns: **Isolate name_Number of BLAST hits_Number of clusters_Predicted type_Position in assembly_Possible imposters_Imposters position in assembly_Answer's EMM cluster**,
where the positions are presented in <contig_number>:<position_in_contig>.

The visual result returns an ASCII map of the emm-types in the genome. Types in a single contig are separated with "-", each representing 500bp distance from each other. Types found in different contigs are separated with tab.

The types are presented with flags when something is not right, the possible flags for now being:

| Flag | Description | Additional Information |
| ------ | ------ | ------ |
| * | Suspect Imposter | Types acknowledged in the CDC database as possibly not emm |
| ~ | Imperfect score | Match score below 100% |

Example for all result format:

```
Isolate1	1	EMM65.0	E6
Isolate2	3	EMM4.0	EMM236.3*;EMM156.0*	E1
Isolate3	2	EMM52.1	EMM134.2*	D4

Isolate1	6	1	EMM65.0	5:82168	E6
Isolate2	8	3	EMM4.0	2:104111	EMM236.3*;EMM156.0*	2:102762;2:105504	E1
Isolate3	5	2	EMM52.1	14:10502	EMM134.2*	5:913	D4

Isolate1	EMM65.0
Isolate2	EMM156.0*--EMM4.0--EMM236.3*
Isolate3	EMM52.1	EMM134.2*
```

## BLAST or PCR?

If you are not sure which pipeline to choose from, I recommend using `blast` first, and use `pcr` when you want to check if anything weird is happening in your `blast` result.

An example problem where this might be useful is when there are too much hits reported by emmtyper.

An important thing to note is that not all emm-like can be caught in the conventional PCR typing. PCR pipeline here can be used to see which hits would be returned in the setting of a conventional typing. This is however not fail-proof, as in silico PCR fails when the two primers do not align in the same contig. Better assembly would resolve this problem.

## Contact

Should you want to fill issues or contact me about anything regarding emmtyper,
you can reach me here or on my email: andre.sutanto.91@gmail.com.
