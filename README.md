# mini_project
This is a python scrpit which will assemble, annotate and map the genome reads from a resequencing project of Escherichia coli K-12 strain. The raw read data can be found at https://www.ncbi.nlm.nih.gov/sra/SRX5005282 however downloading it is not necessary for the script to run.

## Required Software:
This script will be using wrappers to call specific bioinformatics tools that must be downloaded and installed before the script can function properly.

fastq-dump (part of sra tools) https://github.com/ncbi/sra-tools  
SPAdes http://cab.spbu.ru/software/spades/  
SAM Tools https://github.com/samtools/samtools  
Prokka https://github.com/tseemann/prokka  
The Tuxedo Suite:  
* BowTie2 http://bowtie-bio.sourceforge.net/index.shtml  
* TopHat2 http://ccb.jhu.edu/software/tophat/index.shtml  
* Cufflinks http://cole-trapnell-lab.github.io/cufflinks  

## Running The Script
The script will automatically download all the necessary data files for you, no need to download them yourself.  The files are available to view in the Sample_Data folder of this GitHub.  
To run the script simply download the python file and run it in your Mac or Linux terminal.    
**example:**  
`python3 OptionA_Jared_Jurss_Code.py`

## Outputs
The script will create a directory called OptionA_Jared_Jurss in whatever directory the python file is run in.  Inside this directory will be a file called OptionA.log, this is a text file which will log the commands used to run SPAdes and Prokka in the terminal as well as result statistics from those programs.  Inside OptionA_Jared_Jurss a directory called SRR8185310_Assembly will be created, this has all the output files from the SPAdes assembly.  Another directory will be made called prokka_results which will contain all the output files from the Prokka annotation.  A direcory called TopHat_files will be created, this will be where the reads and the complete Escherichia genome will be stored for the TopHat mapping.  All the results from the TopHat run will be stored in a directory named SRR1411276_output inside of the TopHat_files diirectory.  This directory will also contain the output files from Cufflinks.  Finally, a file named Option1.fpkm will be created in the OptionA_Jared_Jurss directory.  This is a CSV file which contains the seqname, start, end, strand, and FPKM values for every gene that was mapped.
