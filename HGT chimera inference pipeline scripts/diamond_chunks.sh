#!/bin/bash
#SBATCH -p bigmem # Partition to submit to (comma separated)
#SBATCH -J diamond # Job name
#SBATCH -n 64 # Number of cores
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH --mem 450G
#SBATCH -t 2-00:00
#SBATCH --mail-user=rkapoor@g.harvard.edu
#SBATCH --mail-type=END 
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=FAIL
#singularity exec /cvmfs/singularity.galaxyproject.org/d/i/diamond:2.0.15--hb97b32f_1 
singularity exec /cvmfs/singularity.galaxyproject.org/d/i/diamond:2.0.15--hb97b32f_1 diamond blastp --db /n/holyscratch01/extavour_lab/Lab/rkapoor/dbs/nr.dmnd  --query /n/holyscratch01/extavour_lab/Lab/rkapoor/combined_dp_hgt.fasta --out /n/holyscratch01/extavour_lab/Lab/rkapoor/dp_hgt_blast --outfmt 6 qseqid sseqid stitle staxids sscinames sphylums skingdoms pident length mismatch gapopen qstart qend sstart send evalue bitscore --threads 64 --evalue 10  -k0 --very-sensitive --taxonmap /n/holyscratch01/extavour_lab/Lab/rkapoor/dbs/prot.accession2taxid.gz