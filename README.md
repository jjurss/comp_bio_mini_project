# mini_project
This is a python scrpit which will assemble and annotate the genome reads from a resequencing project of Escherichia coli K-12 strain. The raw read data can be found at https://www.ncbi.nlm.nih.gov/sra/SRX5005282 however downloading it is not necessary for the script to run.

## Required Spftware:
This script will be using wrappers to call specific bioinformatics tools that must be downloaded and installed before the script can function properly.

fastq-dump (part of sra tools) https://github.com/ncbi/sra-tools \n
SPAdes http://cab.spbu.ru/software/spades/ \n
SAM Tools https://github.com/samtools/samtools \n
Prokka https://github.com/tseemann/prokka \n
The Tuxedo Suite: BowTie2 http://bowtie-bio.sourceforge.net/index.shtml \n
                  TopHat2 http://ccb.jhu.edu/software/tophat/index.shtml \n
                  Cufflinks http://cole-trapnell-lab.github.io/cufflinks/ \n

## Running The Script
The script will automatically download all the necessary data files for you, no need to download them yourself.  The files are available to view in the Sample_Data folder of this GitHub.
To run the script simply download the python file and run it in your Mac or Linux terminal.  
example: "python3 OptionA_Jared_Jurss_Code.py"
The script will create a directory called OptionA_Jared_Jurss in whatever directory it is run in.  Inside this directory will be a file called OptionA.log, this is a text file which will log the commands used to run SPAdes and Prokka in the terminal.  It will also output some of the result statistics from these programs.  Inside OptionA_Jared_Jurss a directory called SRR8185310_Assembly will be created, this has all the output files from SPAdes.  Inside this directory will be another directory called prokka_results which will contain all the output files from Prokka.     
