# Arthropod-HGT-Chimeras description of scripts and outputs (in order)	
## chromosome_scaffold_level.csv
genome assembly refseq accessions, genome quality data and taxonomic info
## download_genomes.sh
download genome from ncbi (refseq accession is the parameter). 
## get_cds_by_scaffold.sh 
Filter each genome using GFF3 and fasta: throw out all scaffolds < 100 kb but add back mitochondria. Takes genome name 
## Concat.sh
Merge all into a single fasta, appending  assembly name to each prot accession
## mmseq2_makedb.sh
convert fasta into an mmseqs2 database
## mmseq2_cluster80.sh
cluster with 80% mutual coverage cutoff and 1e-3 e-value
## diamond_80.sh
run diamond blastp w/ e-val 10 against nr w/mmseq2 representative sequences as queries
## split_blast_table.sh
splits diamond output table by query value. Takes output_dir, input_file as parameters (run on diamond_80 output)
## interval_candidates_shared.py
Runs interval demarcation algorithm (Bréhélin et al. PLOS Computational Biology, 2018) then applies HGT ancestry annotation to each interval. Input: name of a df in inter_blast_results directory (for a single query). Writes all metazoan and HGT intervals to "all_interval_results_shared.txt"
## chimera_overlap_detection.py
identifies putative chimeras as >=1 meta AND >=1 HGT interval in the same query. Ensures non-arthropod hits to HGT and meta intervals are not overlapping and full length homologs are not found outside arthropods.
## write_interval_fasta.py
write a separate fasta with separate entries for each meta and HGT interval in putative chimeras from step 10
## diamond_chunks.sh
run round 2 diamond blastp w/ separated intervals as queries
## split_blast_table.sh
splits diamond output table by query value. Takes output_dir, input_file as parameters (run on diamond_chunks output)
## interval_blast_annot.py
checks the output of round2 blast, reannotates intervals as “HGT”, “Meta” or None and outputs confirmed HGT and Meta intervals to “meta_incl.txt” and “hgt_incl.txt”
## build_inter_hmms.py
uses arthropod blast hits from round 2 blast to build MSAs and profile HMMs for each interval confirmed in step 14. Profiles and MSAs stored in “hmmer_results”
## concat_hmms.sh
concatenate profile HMMs from “hmmer_results” into a 50 files (such that each concatenated file runs in less than 1 day with hmmsearch)
## hmmer_to_phylo.ipynb
identifies and confirms secondary chimeras from concat_hmms.sh. Makes a phylogenetic dataset, builds MSA and runs iQ-tree for each interval.
## pipeline_final/root_annotate_upload_trees.ipynb
roots iQ-tree ML trees with minimum ancestor deviation (Dagan et al. Nature ecology and evolution, 2017 https://doi.org/10.1038/s41559-017-0193) and uploads to iTOL with appropriate tree annotation files (colorstrip, taxonomic information, and sequence descriptions).

