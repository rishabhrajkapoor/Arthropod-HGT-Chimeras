# Arthropod-HGT-Chimeras 

## HGT chimera inference pipeline scripts 
### nr_dbs
Scripts to download NCBI NR and associated taxonomic information, and make an indexed diamond blast database as well as standard blast database. Call scripts in this order: download_nr.sh, download_tax.sh, diamond_db.sh, makeblastdb.sh. The standard blast database is solely used for efficient sequence lookup using the script query_nr_protein.sh, which takes takes two inputs: 1. a protein accession, 2. a fasta output file to append to protein fasta to. 
### tax_pkg 
Scripts to make ("make_sql_tax.py", called by "make_sql.sh") a sql database for efficient lookup of taxonomic information from nr protein accessions. "accession2taxid.py" can be imported into other notebooks to access the function "get_taxid", which takes as an NCBI NR protein accession and returns a taxid. "taxid.py" contains a function get_lineage, which takes a taxid and looks up its Linnaean lineage in the NR "nodes.dmp" and "names.dmp" files.

### chromosome_scaffold_level.csv
genome assembly refseq accessions, genome quality data and taxonomic info
### download_genomes.sh
download genome from ncbi (refseq accession is the parameter). 
### get_cds_by_scaffold.sh 
Filter each genome using GFF3 and fasta: throw out all scaffolds < 100 kb but add back mitochondria. Takes genome name 
### Concat.sh
Merge all into a single fasta, appending  assembly name to each prot accession
### mmseq2_makedb.sh
convert fasta into an mmseqs2 database
### mmseq2_cluster80.sh
cluster with 80% mutual coverage cutoff and 1e-3 e-value
### diamond_80.sh
run diamond blastp w/ e-val 10 against nr w/mmseq2 representative sequences as queries
### split_blast_table.sh
splits diamond output table by query value. Takes output_dir, input_file as parameters (run on diamond_80 output)
### interval_candidates_shared.py
Runs interval demarcation algorithm (Bréhélin et al. PLOS Computational Biology, 2018) then applies HGT ancestry annotation to each interval. Input: name of a df in inter_blast_results directory (for a single query). Writes all metazoan and HGT intervals to "all_interval_results_shared.txt"
### chimera_overlap_detection.py
identifies putative chimeras as >=1 meta AND >=1 HGT interval in the same query. Ensures non-arthropod hits to HGT and meta intervals are not overlapping and full length homologs are not found outside arthropods.
### write_interval_fasta.py
write a separate fasta with separate entries for each meta and HGT interval in putative chimeras from step 10
### diamond_chunks.sh
run round 2 diamond blastp w/ separated intervals as queries
### split_blast_table.sh
splits diamond output table by query value. Takes output_dir, input_file as parameters (run on diamond_chunks output)
### interval_blast_annot.py
checks the output of round2 blast, reannotates intervals as “HGT”, “Meta” or None and outputs confirmed HGT and Meta intervals to “meta_incl.txt” and “hgt_incl.txt”
### build_inter_hmms.py
uses arthropod blast hits from round 2 blast to build MSAs and profile HMMs for each interval confirmed in step 14. Profiles and MSAs stored in “hmmer_results”
### concat_hmms.sh
concatenate profile HMMs from “hmmer_results” into a 50 files (such that each concatenated file runs in less than 1 day with hmmsearch)
### hmmer_array.sh
runs HMMsearch on the concatenated profile HMMs generated in concat_hmms.sh
### split_hmmer_csv.sh
splits HMMer outputs into individual csv files per query
### hmmer_to_phylo.ipynb
identifies and confirms secondary chimeras from concat_hmms.sh. Makes a phylogenetic dataset, builds MSA and runs iQ-tree for each interval.
### align_iq_pipe.sh
runs MUSCLE on the fasta file of HMMER hits to an interval, followed by MSA trimming with trimAl (remove columns with gaps in >40% of sequences), and maximum likelihood phylogenetics with IQ-tree (automated model selection with 1000 bootstraps). Called from within hmmer_to_phylo.ipynb
### root_annotate_upload_trees.ipynb
roots iQ-tree ML trees with minimum ancestor deviation (Dagan et al. Nature ecology and evolution, 2017 https://doi.org/10.1038/s41559-017-0193) and uploads to iTOL with appropriate tree annotation files (colorstrip, taxonomic information, and sequence descriptions).
### species_distribution.ipynb
Consolidate final list of chimeric HGT candidates from manual tree annotation; makes a dataframe storing data (accession, description, taxonomic distribution) for each chimera; determines the taxonomic span of each HGT-chimera; clusters HGT-Chimeras into orthologous groups using a network approach. Outputs cluster_info.tsv, which contains data for each orthologous cluster, and protein_info.csv, which contains data for each protein.
### protein_info.csv 
Information on the taxonomic range  of each hgt-chimera 
## downstream_analysis_and_figures
Contains scripts to analyze the evolutionary history and molecular features of identified HGT-chimeras (duplication, gc content, codon bias, dn/ds, taxonomic distribution, HGT origins,etc.). Also contains plotting scripts for figures in the publication.
Information on the taxonomic range of each orthologous cluster of hgt-chimeras
### blastplot1.py
Python script to generate plots visualizing the taxomic distribution of blast hits from the first round of blast (with whole protein sequences as queries). Accesses chimera interval annotations stored in "chimera_intervals_final.pickle" and DIAMOND blast results in .tsv format stored in "blast_round_one_data." Blast results are available on the Dryad repository. Used to generate Figure 1A, SI figure 2A, SI figure 3B, and supplementary pdf 1. 
### blastplot2.py
Python script to generate plots visualizing the taxomic distribution of blast hits from the second round of blast (with separated HGT/metazoan intervals as queries).  Accesses chimera interval annotations stored in "chimera_intervals_final.pickle" and DIAMOND blast results in .tsv format stored in "blast_round_two_data." last results are available on the Dryad repository. Used to generate Figure 1A,SI figure 3B, and supplementary pdf 1. 
### compile_blastplot_pdf.ipynb
Compiles round one and round two blast plots into a single PDF.

### methods_figure_panel.ipynb
Generated figure illustrating interval demarcation algorithm. Used for SI figure 2. 

### upload_final_trees_to_itol_add_legend.ipynb
Upload the final filtered set of trees to the iTOL webserver for publication. Uses the annotation files and newick trees generated in the main inference pipeline ("HGT chimera inference pipeline scripts
/root_annotate_upload_trees.ipynb" and adds a legend for the taxonomic color assignments. Results are available at https://itol.embl.de/shared/rkapoor 

### updated_taxonomic_distribution_fig.ipynb
Tabulates and plots information on the number of HGT-chimeras/genome (figure 2A), chimera distribution across taxonomic class (SI figure 4), and the taxonomic range of chimeras (SI figure 5). Data stored in supplementary tables II-IV. 

### hgt_origins_analysis.ipynb
Tabulate and plot information related to the taxonomic origin of HGT intervals and their putative origins in symbionts (Figure 3 and supplementary table IV). 

### within_genome_parent_v2.ipynb
Run within-genome DIAMOND blastp searches for parent genes and perform analysis for tandem duplicates/retroduplicates (Figure 4). Calls the scripts "make_genome_db.sh" and "run_diamond_query.sh" for within-genome DIAMOND search. Outputs in supplementary table VIII. 

### codon_and_gc_content_analysis.ipynb
Compare the GC content and codon use of HGT and metazoan regions (Figure 5A). Outputs in supplementary table IX. 

### expression_support.ipynb

Script to obtain information on rna-seq vs ab initio support for HGT-chimeras (supplementary table X).

### dnds_analysis
Contains two notebooks to run dn/ds analyses with PAML: 1. gene_wide_partition_dnds.ipynb runs the M0 (gene-wide model) and partition models (PAML option G); 2. genus_speicies_branch_dnds.ipynb. Both call scripts and codeml configuration files in "dnds_analysis/dnds_scripts." Generates figures 5D-G. Outputs stored in supplementary tables XII-XIV.

### plot_go_terms.ipynb
Plots manually-curated gene functional annotations (SI Figure 8), from data in SI table XV.

### cluster2_percent_identity.ipynb
Plots heatmap of pairwise nucleotide identity for codon-aligned CDS sequences in HGT-chimera orthologous cluster 2 (SI Figure 6). Codon alignment is available on Dryad. 
