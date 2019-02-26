import os
from Bio import SeqIO
## creates the working directory for the scrpit
os.mkdir("OptionA_Jared_Jurss")
os.chdir("OptionA_Jared_Jurss")
## creates the log file for the scrpit
log = open("OptionA.log", "w")
## Downloading the reads for the K-12 resequencing project via the backend of NCBI
os.system("wget ftp://ftp.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/SRR818/SRR8185310/SRR8185310.sra")
reads_file = "SRR8185310.sra"
## fastq-dump is used to decompress the .sra file of the reads into a .fastq file for the assembler
os.system("fastq-dump " + reads_file)
fastq_file = "SRR8185310.fastq"
## This is the command which will call SPAdes to do the assembly
## The values for -k are seeds for the alogorithm
## The value for -t is the number of threads the assembler can use, can be changed based upon system specifications (more = faster)
## -o is the output directory for the results of the assembly
SPAdes_command = "spades -k 55,77,99,127 -t 6 --only-assembler -s " + fastq_file + " -o SRR8185310_Assembly/"
log.write(SPAdes_command + " \n")
os.system(SPAdes_command)
## This is the handle for the assembled contig file
contig_handle = "SRR8185310_Assembly/contigs.fasta"
contigs = SeqIO.parse(contig_handle, "fasta")
significant_contigs = []
count = 0
## Determines whether contigs are of a significant lenght (1000 bp) and counts the number of significant contigs
for record in contigs:
    if len(record.seq) > 1000:
        significant_contigs.append(record)
        count += 1
log.write("There are " + str(count) + " contigs > 1000bp in the assembly. \n")
assembly_length = 0
## Sums the lengths of all the significant contigs to find the total length of the assembly
for contig in significant_contigs:
    assembly_length += len(contig)
log.write("There are " + str(assembly_length) + " bp in the assembly. \n")
## This is the command which calls Prokka to annotate the assembly
## --outdir gives the outdirectory for the results
## --prefix is the name of all the output files created
## --genus is the database being used by Prokka to annotate the assembly
## --mincontiglen is the minimum length for a contig to be considered
prokka_commmand = "prokka --outdir prokka_results --prefix Ecoli --genus Escherichia --mincontiglen 1000 SRR8185310_Assembly/contigs.fasta"
log.write(prokka_commmand + " \n")
os.system(prokka_commmand)
prokka_results = open("prokka_results/Ecoli.txt").readlines()
## Writes the results of the Prokka run as text in the log file
for line in prokka_results:
    log.write(line)
## Storing the number of CDS and tRNAs Prokka found in the assembly for comparison to the accepted values.
CDS = int(prokka_results[4].strip().split(" ")[1])
tRNA = int(prokka_results[5].strip().split(" ")[1])
## Compares the number of CDS and tRNAs to the accepted values for this genome (4140 CDS and 89 tRNAs)
## Writes the discrepencies to the log file
if CDS > 4140:
    log.write("Prokka found an additional " + str(CDS - 4140) + " CDS")
else:
    log.write("Prokka found " + str(4140 - CDS) + " fewer CDS")
if tRNA > 89:
    log.write(" and " + str(tRNA - 89) + " additional tRNA")
else:
    log.write(" and " + str(89 - tRNA) + " fewer tRNA")
os.mkdir("TopHat_files")
os.chdir("TopHat_files")
## Downloads the complete annotated genome of Escherichia coli
os.system("wget ftp://ftp.ncbi.nlm.nih.gov/genomes/archive/old_refseq/Bacteria/Escherichia_coli_K_12_substr__MG1655_uid57779/NC_000913.fna")
## Downloads the reads for the E. coli transcriptome project of a K-12 derivative (BW38028)
os.system("wget ftp://ftp.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/SRR141/SRR1411276/SRR1411276.sra")
## Builds a BowTie2 index from the complete genome for use with TopHat2
os.system("bowtie2-build NC_000913.fna NC_000913")
## Calls fastq-dump to decompress the .sra file of the K-12 reads
os.system("fastq-dump -I --split-files SRR1411276.sra")
## Calls TopHat2 to perform the mapping
## -o is the output directory for the TopHat run
## -p is the number of threads being used for the mapping, can be changed based on system specifications
os.system("tophat2 -o SRR1411276_output --no-novel-juncs -p 6 NC_000913 SRR1411276_1.fastq")
os.chdir("SRR1411276_output")
## Calls Cufflinks
## -o is the output directory
## -p is the number of threads being used, can be changed based on system specifications
os.system("cufflinks -o cufflinks_output -p 6 accepted_hits.bam")
## Opens the results of the Cufflinks run for parsing
data = open("cufflinks_output/transcripts.gtf").readlines()
os.chdir("..")
os.chdir("..")
output = open("Option1.fpkm", "w")
## Iterates through the results of the Cufflinks run
## Writes the desired data (seqname, start, end, strand, and FPKM value) to Option1.fpkm
## This is a CSV file where each row is a gene
for line in data:
    line_data = line.split("\t")
    output.write(line_data[0] + ", " + line_data[3] + ", " + line_data[4] + ", " + line_data[6] + ", ")
    attributes = line_data[8].split("; ")
    for attribute in attributes:
        if "FPKM" in attribute:
            output.write(attribute + " \n")
log.close()
output.close()
