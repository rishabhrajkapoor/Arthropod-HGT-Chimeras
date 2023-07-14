#!/bin/bash
#SBATCH -p shared # Partition to submit to (comma separated)
#SBATCH -J runhmm # Job name
#SBATCH -n 20 # Number of cores
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH --mem 100G
#SBATCH -t 0-7:00
#SBATCH --mail-user=rkapoor@g.harvard.edu
#SBATCH --mail-type=END 
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=FAIL
#SBATCH --array=1-50  # Size of the array

module load Anaconda3/2020.11
source activate rishabh

hmmsearch --cpu 20 --domtblout "meta_concat_hmms/${SLURM_ARRAY_TASK_ID}_domt" "meta_concat_hmms/${SLURM_ARRAY_TASK_ID}" "/n/holyscratch01/extavour_lab/Lab/rkapoor/dbs/nr.fasta" > hmm_meta.out
