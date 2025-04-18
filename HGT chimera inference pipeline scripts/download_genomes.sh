#!/bin/bash
#SBATCH -p shared # Partition to submit to (comma separated)
#SBATCH -J diamond # Job name
#SBATCH -n 10 # Number of cores
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH --mem 10G
#SBATCH -t 1-00:00
#SBATCH --mail-user=rkapoor@g.harvard.edu
#SBATCH --mail-type=FAIL
module load Anaconda3/2020.11
source activate rishabh 
cd scaffold_genomes

curl -OJX GET "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/$1/download?include_annotation_type=GENOME_GFF,PROT_FASTA,SEQUENCE_REPORT&filename=$1.zip" -H "Accept: application/zip" 

unzip -o $1.zip
