#!/bin/bash
#SBATCH -p bigmem # Partition to submit to (comma separated)
#SBATCH -J makedb # Job name
#SBATCH -n 35 # Number of cores
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH --mem 350G
#SBATCH -t 1-00:00
#SBATCH --mail-user=rkapoor@g.harvard.edu
#SBATCH --mail-type=END 
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=FAIL

cd nr_blastdb
module load centos6
module load blast/2.2.29+-fasrc01
update_blastdb.pl --decompress nr