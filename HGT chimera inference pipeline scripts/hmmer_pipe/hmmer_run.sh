#!/bin/bash
#SBATCH -p shared # Partition to submit to (comma separated)
#SBATCH -J runhmm # Job name
#SBATCH -n 20 # Number of cores
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH --mem 100G
#SBATCH -t 1-00:00
#SBATCH --mail-user=rkapoor@g.harvard.edu
#SBATCH --mail-type=END 
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=FAIL

module load Anaconda3/2020.11
source activate rishabh

cd $1

module load muscle/3.8.31-fasrc01
muscle -in sub_seq.fasta -out MSA_sub_seq.fasta

# #build hmm 
singularity exec /cvmfs/singularity.galaxyproject.org/h/m/hmmer:3.3.2--he1b5a44_0 hmmbuild sub_seq.hmm MSA_sub_seq.fasta

# #run hmmscan
singularity exec /cvmfs/singularity.galaxyproject.org/h/m/hmmer:3.3.2--he1b5a44_0 hmmsearch --cpu 20   -A "hmm_align" --tblout "hmmtbl" --domtblout "domt" sub_seq.hmm "/n/holyscratch01/extavour_lab/Lab/rkapoor/dbs/nr.fasta" >hmm.out 

# #convert hmmer output to fasta file of hits
# python3 /n/holyscratch01/extavour_lab/Lab/rkapoor/hmmer_pipe/get_hmm_fasta.py 

# #run msa
# module load muscle/3.8.31-fasrc01
# muscle -in hmm_output_final.fasta -out MSA_hmm_output_final.fasta

# #trim msa
# module load trimal/1.2rev59-fasrc01
# trimal -in MSA_hmm_output_final.fasta -out trimmed_MSA_hmm_output_final.fasta -gt 0.7 

# #time rev model
# singularity exec /cvmfs/singularity.galaxyproject.org/i/q/iqtree:2.2.0.3--hb97b32f_0 iqtree2 -s trimmed_MSA_hmm_output_final.fasta -B 1000 -T AUTO --prefix rev_aa

# # #nonrev model 
# # singularity exec /cvmfs/singularity.galaxyproject.org/i/q/iqtree:2.2.0.3--hb97b32f_0 iqtree2 -s trimmed_MSA_hmm_output_final.fasta --model-joint NONREV --root-test -zb 10000 -au -te rev_aa.treefile --prefix nonrev_test_rev

# #madroot
# python3 /n/holyscratch01/extavour_lab/Lab/rkapoor/MAD/MAD_root.py 


