#!/bin/bash
#SBATCH -p shared # Partition to submit to (comma separated)
#SBATCH -J runhmm # Job name
#SBATCH -n 30 # Number of cores
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH --mem 100G
#SBATCH -t 1-00:00
#SBATCH --mail-user=rkapoor@g.harvard.edu
#SBATCH --mail-type=END 
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=FAIL

module load Anaconda3/2020.11
source activate rishabh

module load muscle/3.8.31-fasrc01
muscle -in $1 -out muscle_$1

singularity exec /cvmfs/singularity.galaxyproject.org/h/m/hmmer:3.3.2--he1b5a44_0 hmmbuild $1_hmm muscle_$1

singularity exec /cvmfs/singularity.galaxyproject.org/h/m/hmmer:3.3.2--he1b5a44_0 hmmsearch --cpu 30 -A $1_hmm_align --tblout $1_hmmtbl --domtblout $1_domt $1_hmm "/n/holyscratch01/extavour_lab/Lab/rkapoor/dbs/nr" >$1_hmm.out 