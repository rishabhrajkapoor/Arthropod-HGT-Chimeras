import pickle
import pandas as pd
import multiprocessing as mp
import numpy as np
import pickle
from Bio import SeqIO
import os
import subprocess
import ast

record_dict=SeqIO.to_dict(SeqIO.parse('interval_sep_fasta', 'fasta'))

#takes a tuple (query, output_fasta)
#query nr for query (n[0]), write to output fasta (n[2]).
def get_fasta(n):
    n1=n[0]
    n2=n[1]
    subprocess.run(["sh","query_nr_protein.sh",n1,n2])
    return n

#write a copy of fasta_file (str) with all intervals in blast df to output_file (str)
#written by chatGPT and RK
def copy_fasta_with_substr(fasta_file, df, output_file):
    with open(output_file, "w") as out_handle:
        for seq_record in SeqIO.parse(fasta_file, "fasta"):
            seq_name = seq_record.id
       
            if seq_name in df["sseqid"].values:
                sub_df = df[df["sseqid"] == seq_name]
                for _, row in sub_df.iterrows():
                    sstart = row["sstart"]
                    send = row["send"]
                    subseq = seq_record.seq[sstart-1:send]
                    subseq_name = f"{seq_name}_{sstart}_{send}"
                    subseq_record = seq_record
                    subseq_record.id = subseq_name
                    subseq_record.description = ""
                    subseq_record.seq = subseq
                    SeqIO.write(subseq_record, out_handle, "fasta")
                    
#run MUSCLE to get MSA for multi-seq fasta n (str)
def get_muscle(n):
    gene=";".join(n.split(";")[0:2])
    a=subprocess.run(["sh","hmmer_pipe/muscle.sh", f"hmmer_results/{gene}/{n}"])
    
#run hmm_build to obtain HMMER profile HMM for MSA for query n     
def get_hmm_profile(n):
    gene=";".join(n.split(";")[0:2])
    a=subprocess.run(["sh","hmmer_pipe/hmmbuild.sh", f"hmmer_results/{gene}/{n}"])
    
#takes the name of an interval 
#writes sequences of arthropod blast hits with >30% coverge of interval and e-value < min e-value of non-arthropod hits to fasta 
#runs MUSCLE to make a MSA, then builds profile HMM
def write_fastas_run_hmm(n):
    inter=ast.literal_eval(n.split("_")[3].replace(".tsv",""))
    df=pd.read_csv(f"blast2_inter_split/{n}.tsv",sep="\t", names="qseqid sseqid stitle staxids sscinames sphylums skingdoms pident length mismatch gapopen qstart qend sstart send evalue bitscore".split(" "))
    gene=";".join(n.split(";")[0:2])
    df["cover"]=(np.array(df.qend)-np.array(df.qstart)+1)/len(record_dict[n].seq)
    df=df[df.cover>.30]
    df=df[df.staxids.astype(str)!="32630"]
    arth=df[df.astype(str).sphylums.str.contains("Arthropoda")]
    non_arth=df[~df.astype(str).sphylums.str.contains("Arthropoda")]
    arth=arth[arth.evalue<=non_arth.evalue.min()]
    try:
        os.mkdir(f"hmmer_results/{gene}")
    except:
        p=1
    try:
        os.mkdir(f"hmmer_results/{gene}/{n}")
    except:
        p=1

    for f in [(x,f"hmmer_results/{gene}/{n}/seqf.fasta") for x in arth.sseqid]:
        get_fasta(f)
    with open(f"hmmer_results/{gene}/{n}/seq.fasta", "w") as outfile:
    # Run awk command and redirect output to outfile
        subprocess.run(["awk", "-f", "hmmer_pipe/remove_redundant_seqs.awk", f"hmmer_results/{gene}/{n}/seqf.fasta"], stdout=outfile)
    copy_fasta_with_substr(f"hmmer_results/{gene}/{n}/seq.fasta",arth,f"hmmer_results/{gene}/{n}/sub_seq.fasta")
    get_muscle(n)
    get_hmm_profile(n)
    
    return

f=open("meta_incl.txt","r").readlines()
fs=[x.strip("\n") for x in f]
with mp.Pool(29) as p:
    meta2 = p.map(write_fastas, fs)

f=open("hgt_incl.txt","r").readlines()
fs=[x.strip("\n") for x in f]
with mp.Pool(29) as p:
    meta2 = p.map(write_fastas, fs)