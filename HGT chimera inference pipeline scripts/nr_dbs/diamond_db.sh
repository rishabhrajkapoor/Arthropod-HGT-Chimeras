#!/bin/bash
#SBATCH -p bigmem # Partition to submit to (comma separated)
#SBATCH -J diamond_db # Job name
#SBATCH -n 50 # Number of cores
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH --mem 300G
#SBATCH -t 2-00:00
#SBATCH --mail-user=rkapoor@g.harvard.edu
#SBATCH --mail-type=END 
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=FAIL

singularity exec /cvmfs/singularity.galaxyproject.org/d/i/diamond:2.0.15--hb97b32f_1 diamond makedb --in '/n/holyscratch01/extavour_lab/Lab/rkapoor/dbs/nr.fasta' --db '/n/holyscratch01/extavour_lab/Lab/rkapoor/dbs/nr' --taxonmap '/n/holyscratch01/extavour_lab/Lab/rkapoor/dbs/prot.accession2taxid.gz' --taxonnodes '/n/holyscratch01/extavour_lab/Lab/rkapoor/dbs/nodes.dmp' --taxonnames '/n/holyscratch01/extavour_lab/Lab/rkapoor/dbs/names.dmp' --threads 50