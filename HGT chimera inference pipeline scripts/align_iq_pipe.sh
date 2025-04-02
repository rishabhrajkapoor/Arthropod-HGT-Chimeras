#!/bin/bash
#SBATCH -p shared # Partition to submit to (comma separated)
#SBATCH -J diamond # Job name
#SBATCH -n 30 # Number of cores
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH --mem 25G
#SBATCH -t 3-00:00
#SBATCH --mail-user=rkapoor@g.harvard.edu
#SBATCH --mail-type=FAIL

cd "/n/holyscratch01/extavour_lab/Lab/rkapoor/hmmer_phylo_data"/$1

singularity exec /cvmfs/singularity.galaxyproject.org/m/u/muscle:5.1--h4ac6f70_3 muscle -align sub_phylo_tax.fasta -output MSA_hmm_output_final.fasta

singularity exec /cvmfs/singularity.galaxyproject.org/t/r/trimal:1.4.1--h9f5acd7_7 trimal -in MSA_hmm_output_final.fasta -out trimmed_MSA_hmm_output_final.fasta -gt 0.6 

sbatch "/n/home11/rkapoor/pipeline_final/"iqtree.sh $1