#!/bin/bash
#SBATCH -p shared # Partition to submit to (comma separated)
#SBATCH -J paml # Job name
#SBATCH -n 25 # Number of cores
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH --mem 10G
#SBATCH -t 1-00:00
#SBATCH --mail-user=rkapoor@g.harvard.edu
#SBATCH --mail-type=FAIL

cp dnds/$1/tree.newick  dnds/$1/$2/tree.newick

cd dnds/$1/$2

singularity exec /cvmfs/singularity.galaxyproject.org/p/a/paml:4.10.6--h031d066_1 codeml /n/home11/rkapoor/pipeline_final/dnds_scripts/m2_codeml.ctl

singularity exec /cvmfs/singularity.galaxyproject.org/p/a/paml:4.10.6--h031d066_1 codeml /n/home11/rkapoor/pipeline_final/dnds_scripts/m4_codeml.ctl
