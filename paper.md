---
title: 'emmtyper: A tool for in silico EMM typing of Streptococcus pyogenes'
tags:
  - Python
  - Bioinformatics
  - Microbial Genomics
  - Public Health Microbiology
  - Molecular Epidemiology
authors:
  - name: Andre Tan
    affiliation: "1, 2"
  - name: Torsten Seemann
    orcid: 0000-0001-6046-610X
    affiliation: "2, 3"
  - name: Jake A. Lacey
    orcid: 0000-0002-6492-6983
    affiliation: 3
  - name: Liam Mcintyre
    affiliation: 3
  - name: Mark R. Davies
    affiliation: 3
  - name: Hannah Frost
    orcid: 0000-0002-1543-2805
    affiliation: 4
  - name: Pierre R. Smeesters
    affiliation: 4
  - name: Deborah A. Williamson
    affiliation: "2, 3"
  - name: Anders Gonçalves da Silva
    orcid: 0000-0002-2257-8781
    affiliation: 2
affiliations:
 - name: FinAccel Pte Ltd
   index: 1
 - name: Microbiological Diagnostic Unit Public Health Laboratory, Department of Microbiology and Immunology, Peter Doherty Institute for Immunity and Infection, The University of Melbourne
   index: 2
 - name: Department of Microbiology and Immunology, Peter Doherty Institute for Immunity and Infection, The University of Melbourne
   index: 3
 - name: Molecular Bacteriology Laboratory, Université Libre de Bruxelles
   index: 4
date: 30 October 2019
bibliography: paper.bib
---

# Summary

Bacterial pathogen subtyping is a corner-stone of public health microbiology and epidemiology. By classifying bacterial strains at levels below species and sub-species, bacterial subtyping allows public health officials and epidemiologists to identify and track outbreaks, identify particularly virulent strains, and make decisions about vaccination programmes. As public health microbiology transitions to a workflow primarily based on genomic data, there is an increasing need for Bioinformatic tools to perform *in silico* bacterial subtyping. Such tools are essential to enable the carryover of vast troves of historical data and allow for a smooth transition to genomics-based public health.

`emmtyper` is an *in silico* bacterial subtyping tool written in Python for *emm*-typing and *emm*-cluster typing of *Streptococcus pyogenes*, also known as Group A Streptococcus (GAS). *S. pyogenes* is the causative agent of strep throat, necrotizing fasciitis, and Scarlet fever. *emm*-typing targets variation at the *emm* gene that produces the surface antigen known as M protein. The M protein was initially used as a target for GAS subtyping because it is essential for evading the human immune system, and thus essential to the bacteria's virulence. *emm*-cluster typing groups *emm*-types into functionally equivalent clusters, facilitating vaccine development.

Essential to the working of `emmtyper` is a FASTA database of sequences annotated with the M-type. The database consists of a set of sequences typically of 180bp in length that covers a portion of the *emm* gene, and is curated by the CDC *Streptococcus* laboratory ([CDC](https://www2.cdc.gov/vaccines/biotech/strepblast.asp)). The database is updated on a regular basis, adding newly characterized sequences. To ensure the local database used by `emmtyper` is up to date, we provide facilities for the user to check if their database is out-of-date, and if so, to download and update the local database. We check the database integrity by checking for and removing any duplicate sequences using the tool `seqkit` [CITATION]. `emmtyper` keeps a JSON formatted log of database updates, providing the user with a history of changes over time and is what permits the tool to check if the local database is out-of-date.

To give users flexibility about how they wish to use `emmtyper`, we provide two distinct modes of operation: `blast` and *in silico* PCR. The `blast` mode is the default mode of operation, and it blasts the contigs of the assembly supplied by the user against the database of *emm*-type annotated sequences. The `in silico` mode uses the *in silico* PCR tool `isPcr` [CITATION] to identify one or more PCR fragments in the contigs of the assembly suppplied by the user, and then subsequently, the fragments are blasted against the database of *emm*-type annotated sequences. At the moment, two sets of PCR primers are shipped with `emmtyper`, the canonical PCR primers recommended by the CDC M-typing protocol [CITATION], and a set of redesigned primers published more recently by Frost *et al.* [CITATION]. The CDC canonical primers are used by default, but the user is able to select the Frost *et al.* `in silico` PCR primers by setting the `--pcr-primer` option to `frost`. The user is also able to supply their own primers by setting the `--primer-db` to the path to the appropriately formatted file.

`emmtyper` is now routinely used for *emm*-typing and *emm*-cluster typing of *Streptococcus pyogenes* at the Microbiological Diagnostic Unit Public Health Lab, has been used in a number of papers, and has been added to bacterial pathogen Bioinformatic pipelines (e.g., Bactopia). Importantly, the tool has been fully validated and is ready for use in the field. `emmtyper` is available on PyPI, and on Bioconda, to make it easy for the user to install the tool. 

Transition to genomics in public health.

Bacterial subtyping in public health.

EMM typing in GAS.

GAS epidemiology.

Prior use of emmtyper (Lacey).

Statement of need: what it provides: support for transition to genomics. Validated tool.
