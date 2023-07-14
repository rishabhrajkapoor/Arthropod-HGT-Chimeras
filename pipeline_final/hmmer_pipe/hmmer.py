import pickle
import pandas as pd
import multiprocessing as mp
import numpy as np
import pickle
import matplotlib.pyplot as plt
from Bio import SeqIO
import os
import subprocess
import sys

nam=sys.argv[1]

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
                    
inters=os.listdir(f"diamond2_split2/{nam}")
df1=pd.read_csv(f"non_awk_split/{nam}.tsv",sep="\t", names="qseqid sseqid stitle staxids sscinames sphylums skingdoms pident length mismatch gapopen qstart qend sstart send evalue bitscore".split(" "))
df=pd.read_csv(f"diamond2_split2/{nam}/{inters[0]}",sep="\t", names="qseqid sseqid stitle staxids sscinames sphylums skingdoms pident length mismatch gapopen qstart qend sstart send evalue bitscore".split(" "))

for i in inters:
    df=pd.read_csv(f"diamond2_split2/{nam}/{i}",sep="\t", names="qseqid sseqid stitle staxids sscinames sphylums skingdoms pident length mismatch gapopen qstart qend sstart send evalue bitscore".split(" "))
    arth=df[df.astype(str).sphylums.str.contains("Arthropoda")]
    non_arth=df[~df.astype(str).sphylums.str.contains("Arthropoda")]
    arth=arth[arth.evalue<non_arth.evalue.min()]
    os.mkdir(f"hmmer_results/{nam}/{i}")
    for f in [(x,f"hmmer_results/{nam}/{i}/seqf.fasta") for x in arth.sseqid]:
        get_fasta(f)
    with open(f"hmmer_results/{nam}/{i}/seq.fasta", "w") as outfile:
    # Run awk command and redirect output to outfile
        subprocess.run(["awk", "-f", "hmmer_pipe/remove_redundant_seqs.awk", f"hmmer_results/{nam}/{i}/seqf.fasta"], stdout=outfile)
    copy_fasta_with_substr(f"hmmer_results/{nam}/{i}/seq.fasta",arth,f"hmmer_results/{nam}/{i}/sub_seq.fasta")
    subprocess.run(["sbatch","hmmer_pipe/hmmer_run.sh",f"hmmer_results/{nam}/{i}"])