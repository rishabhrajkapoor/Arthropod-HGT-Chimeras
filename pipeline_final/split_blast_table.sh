#!/bin/bash
#SBATCH -p bigmem # Partition to submit to (comma separated)
#SBATCH -J diamond # Job name
#SBATCH -n 10 # Number of cores
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH --mem 300G
#SBATCH -t 0-6:00
#SBATCH --mail-user=rkapoor@g.harvard.edu
#SBATCH --mail-type=END 
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=FAIL
# Create the output directory if it doesn't exist
output_dir="/n/holyscratch01/extavour_lab/Lab/rkapoor/$1"
mkdir -p "$output_dir"

# AWK script to split the TSV file
awk -F'\t' -v output_dir="$output_dir" '{
    # Extract the value of the first column
    value = $1

    # Construct the output file path
    output_file = output_dir "/" value ".tsv"

    # Append the current line to the corresponding output file
    print >> output_file
}' "$2"

echo "Splitting complete. Split files are stored in $output_dir directory."
