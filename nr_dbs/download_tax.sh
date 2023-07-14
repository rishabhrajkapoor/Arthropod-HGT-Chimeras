#!/bin/bash
#SBATCH -p shared # Partition to submit to (comma separated)
#SBATCH -J download_tax # Job name
#SBATCH -n 20 # Number of cores
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH --mem 50G
#SBATCH -t 6-00:00
#SBATCH --mail-user=rkapoor@g.harvard.edu
#SBATCH --mail-type=END 
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=FAIL

# Destination directory for downloaded files
DEST_DIR="/n/holyscratch01/extavour_lab/Lab/rkapoor/dbs"

# URLs for files to download
ACCESSION_URL="ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/prot.accession2taxid.FULL.gz"
NODES_URL="ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz"
NAMES_URL="ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz"

# Change to destination directory
cd "$DEST_DIR"

# Download accession2taxid file and save it to destination directory
echo "Downloading protein accession2taxid file from $ACCESSION_URL..."
curl -o prot.accession2taxid.gz "$ACCESSION_URL"

# # Download taxonomy dump file and extract required files
# echo "Downloading and extracting taxonomy dump files from $NODES_URL..."
# curl -o taxdump.tar.gz "$NODES_URL"
# tar -xzf taxdump.tar.gz names.dmp nodes.dmp

# Unzip the downloaded files
echo "Unzipping downloaded files..."
gunzip -c prot.accession2taxid.gz >accession2taxid.csv

 
echo "Download complete."