#!/bin/bash

#SBATCH -p bigmem # Partition to submit to (comma separated)
#SBATCH -J concat # Job name
#SBATCH -n 10 # Number of cores
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH --mem 300G
#SBATCH -t 1-00:00
cd scaffold_genomes/ncbi_dataset/data
for dir in */; do
  for file in "$dir"output_fasta.fa; do
    if [ -f "$file" ]; then
      sed -i "s/^>/>${dir%%/};/" "$file"
      cat "$file" >> combined_output.fa
    fi
  done
done