#!/bin/bash
#SBATCH -p bigmem # Partition to submit to (comma separated)
#SBATCH -J make_sql # Job name
#SBATCH -n 20 # Number of cores
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH --mem 300G
#SBATCH -t 2-00:00
#SBATCH --mail-user=rkapoor@g.harvard.edu
#SBATCH --mail-type=END 
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=FAIL

module load Anaconda3/2020.11
source activate rishabh
python3 /n/home11/rkapoor/tax_pkg/make_sql_tax.py