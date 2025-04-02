#!/bin/bash
#SBATCH -p serial_requeue # Partition to submit to (comma separated)
#SBATCH -J paml # Job name
#SBATCH -n 25 # Number of cores
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH --mem 25G
#SBATCH -t 3-00:00
#SBATCH --mail-user=rkapoor@g.harvard.edu
#SBATCH --mail-type=FAIL

cd $1/$2

singularity exec /cvmfs/singularity.galaxyproject.org/p/a/paml:4.10.6--h031d066_1 codeml /n/holylabs/LABS/extavour_lab/Users/rkapoor/pipeline_final/dnds_scripts/m0_branch.ctl