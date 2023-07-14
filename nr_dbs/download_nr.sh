#!/bin/bash
#SBATCH -p shared # Partition to submit to (comma separated)
#SBATCH -J align # Job name
#SBATCH -n 20 # Number of cores
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH --mem 50G
#SBATCH -t 6-00:00
#SBATCH --mail-user=rkapoor@g.harvard.edu
#SBATCH --mail-type=END 
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=FAIL

# Destination directory for downloaded file
DEST_DIR="/n/holyscratch01/extavour_lab/Lab/rkapoor/dbs"

# Filename for downloaded file
FILENAME="nr.fasta"

# URL for latest nr FASTA file on NCBI
URL="ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nr.gz"

# Change to destination directory
cd "$DEST_DIR"

# Download file and save it to destination directory
echo "Downloading $URL..."
curl -o "$FILENAME.gz" "$URL"

# Extract the downloaded file from the gzip archive
echo "Extracting $FILENAME.gz..."
gunzip "$FILENAME.gz"

echo "Download complete."
