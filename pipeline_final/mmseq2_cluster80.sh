#!/bin/bash
#SBATCH -p bigmem # Partition to submit to (comma separated)
#SBATCH -J diamond # Job name
#SBATCH -n 40 # Number of cores
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH --mem 450G
#SBATCH -t 1-00:00
#SBATCH --mail-user=rkapoor@g.harvard.edu
#SBATCH --mail-type=FAIL


singularity exec /cvmfs/singularity.galaxyproject.org/m/m/mmseqs2:14.7e284--pl5321hf1761c0_0 mmseqs cluster /n/holyscratch01/extavour_lab/Lab/rkapoor/scaffold_genomes/ncbi_dataset/data/mmseq_combined_output /n/holyscratch01/extavour_lab/Lab/rkapoor/scaffold_genomes/ncbi_dataset/data/mmseq_combined_output_clustered80 /n/holyscratch01/extavour_lab/Lab/rkapoor/tmp -c 0.80 --threads 40