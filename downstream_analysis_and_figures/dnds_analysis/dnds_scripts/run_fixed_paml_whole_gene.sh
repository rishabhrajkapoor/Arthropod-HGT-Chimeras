#!/bin/bash
#SBATCH -p shared # Partition to submit to (comma separated)
#SBATCH -J fixed_paml # Job name
#SBATCH -n 25 # Number of cores
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH --mem 25G
#SBATCH -t 0-08:00
#SBATCH --mail-user=rkapoor@g.harvard.edu
#SBATCH --mail-type=FAIL

cd dnds/$1

singularity exec /cvmfs/singularity.galaxyproject.org/p/a/paml:4.10.6--h031d066_1 codeml /n/holylabs/LABS/extavour_lab/Users/rkapoor/pipeline_final/dnds_scripts/fix_omega_full_gene.ctl