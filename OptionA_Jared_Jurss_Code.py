import os
from Bio import SeqIO
os.mkdir("OptionA_Jared_Jurss")
os.chdir("OptionA_Jared_Jurss")
log = open("OptionA.log", "w")
os.system("wget ftp://ftp.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/SRR818/SRR8185310/SRR8185310.sra")
reads_file = "SRR8185310.sra"
os.system("fastq-dump " + reads_file)
fastq_file = "SRR8185310.fastq"
SPAdes_command = "spades -k 55,77,99,127 -t 2 --only-assembler -s " + fastq_file + " -o SRR8185310_Assembly/"
log.write(SPAdes_command)
os.system(SPAdes_command)
log = open("OptionA.log", "w")
contig_handle = "SRR8185310_Assembly/contigs.fasta"
contigs = SeqIO.parse(contig_handle, "fasta")
significant_contigs = []
count = 0
for record in contigs:
    if len(record.seq) > 1000:
        significant_contigs.append(record)
        count += 1
log.write("There are " + str(count) + " contigs > 1000bp in the assembly. \n")
assembly_length = 0
for contig in significant_contigs:
    assembly_length += len(contig)
log.write("There are " + str(assembly_length) + " bp in the assembly. \n")
prokka_commmand = "prokka --outdir prokka_results --prefix Ecoli --genus Escherichia --mincontiglen 1000 SRR8185310_Assembly/contigs.fasta"
log.write(prokka_commmand)
os.system(prokka_commmand)
prokka_results = open("prokka_results/Ecoli.txt").readlines()
for line in prokka_results:
    log.write(line)
CDS = int(prokka_results[4].strip().split(" ")[1])
tRNA = int(prokka_results[5].strip().split(" ")[1])
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
os.system("wget ftp://ftp.ncbi.nlm.nih.gov/genomes/archive/old_refseq/Bacteria/Escherichia_coli_K_12_substr__MG1655_uid57779/NC_000913.fna")
os.system("wget ftp://ftp.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/SRR141/SRR1411276/SRR1411276.sra")
os.system("bowtie2-build NC_000913.fna NC_000913")
os.system("fastq-dump -I --split-files SRR1411276.sra")
os.system("tophat2 -o SRR1411276_output --no-novel-juncs -p 2 NC_000913 SRR1411276_1.fastq")
os.system("cd SRR1411276_output")
os.system("cufflinks accepted_hits.bam")
data = open("TopHat_Files/SRR1411276_output/transcripts.gtf").readlines()
os.chdir("..")
output = open("Option1.fpkm", "w")
for line in data:
    line_data = line.split("\t")
    output.write(line_data[0] + ", " + line_data[3] + ", " + line_data[4] + ", " + line_data[6] + ", ")
    attributes = line_data[8].split("; ")
    for attribute in attributes:
        if "FPKM" in attribute:
            output.write(attribute + "\n")
log.close()
output.close()
