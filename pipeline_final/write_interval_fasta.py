import pickle
import pandas as pd
import multiprocessing as mp
import numpy as np
import pickle
import matplotlib.pyplot as plt
from Bio import SeqIO
import os
import subprocess
import ast

#load dictionary with query keys and HGT/metazoan intervals 
with open('inter_scan_blast.pickle', 'rb') as handle:
    b = pickle.load(handle)

#write fasta by querying nr for all query accessions
def get_fasta(x):  
    subprocess.run(["sh","query_nr_protein.sh",x.split(";")[1],"inter_queries.fasta"])
with mp.Pool(29) as p:
    hgts = p.map(get_fasta,list(b.keys()))

#write new fasta w/ separated intervals 
record_dict = SeqIO.to_dict(SeqIO.parse('inter_queries.fasta', 'fasta'))
f=open("interval_sep_fasta","w")
for n in b:
    if n.split(";")[1] in record_dict:
        s=record_dict[n.split(";")[1]]
        for interval in b[n]:
            start=interval[0]
            stop=interval[1]
            a=s.seq[max(start-10,0):min(stop+10,len(s.seq))]
            f.write(f'>{n};{b[n][interval]}_{interval}'.replace(" ",""))
            f.write("\n")
            f.write(str(a))
            f.write("\n")
    else:
        for x in record_dict:
            if n.split(";")[1] in record_dict[x].description:
                s=record_dict[x]
                for interval in b[n]:
                    start=interval[0]
                    stop=interval[1]
                    a=s.seq[max(start-10,0):min(stop+10,len(s.seq))]
                    f.write(f'>{n};{b[n][interval]}_{interval}'.replace(" ",""))
                    f.write("\n")
                    f.write(str(a))
                    f.write("\n")
f.close()
