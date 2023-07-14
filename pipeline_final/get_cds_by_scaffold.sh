#!/bin/bash
#!/bin/bash
#SBATCH -p shared # Partition to submit to (comma separated)
#SBATCH -J diamond # Job name
#SBATCH -n 4 # Number of cores
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH --mem 10G
#SBATCH -t 1-00:00



#written by chatgpt and RK
# Set the input file
input_file="scaffold_genomes/ncbi_dataset/data/$1/sequence_report.jsonl"

# Set the field separator to a newline character
IFS=$'\n'
declare -a targets
# Read each line of the file into an array
while read -r line; do
  # Check if the line contains the string "Mitochondrion"
  if echo "$line" | grep -q "Mitochondrion"; then
    refseq_accession=$(echo "$line" | grep -o '"refseqAccession":"[^"]\+"')
    # Extract the value of the refseqAccession field
    refseq_accession="$(echo "$refseq_accession" | cut -d ':' -f 2 | tr -d '"')"
    targets+=("$refseq_accession")
  fi

  # Check if the line contains the string "length:" followed by a number greater than 100000
  length=$(echo "$line" | grep -o '"length":[0-9]\+')
  length="$(echo "$length" | cut -d ':' -f 2)"
  if [ "$length" -gt 100000 ]; then
    refseq_accession=$(echo "$line" | grep -o '"refseqAccession":"[^"]\+"')
    # Extract the value of the refseqAccession field
    refseq_accession="$(echo "$refseq_accession" | cut -d ':' -f 2 | tr -d '"')"
    
    targets+=("$refseq_accession")
  fi
done < $input_file

cd "scaffold_genomes/ncbi_dataset/data/$1"

# Use awk to filter the input file
awk -v targets="${targets[*]}" 'BEGIN {
  split(targets, target_array, " ")
}

# Skip lines starting with "##"
/^##/ {next}

# Process remaining lines
{
  # Extract the first and third items (delimited by tabs)
  first_item=$1
  third_item=$3
  output=$9
  
 
 
  
  # Check if the third item is equal to "CDS"
  if (third_item == "CDS") {
    found=0
    for (i in target_array) {
      if (first_item == target_array[i]) {
        found=1
        break
      }
    }
    
    if (found == 1) {
      print $9 >>"outs.txt"
    }
  }
}' "genomic.gff"

# Store the file name in a variable
file=outs.txt

# Use sed to replace every line in the file
# The sed expression matches everything before "ID=" and after the first ";"
# The expression replaces it with everything after "ID=" and before the first ";"
sed 's/.*ID=cds-\([^;]*\);.*/\1/' $file > temp.txt

# Replace the original file with the modified version
mv temp.txt $file