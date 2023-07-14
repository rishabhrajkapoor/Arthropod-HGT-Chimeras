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

#takes the name of an interval blast dataframe (string) stored in blast2_inter_split
#returns "Meta", "HGT" or none
def check_annot(n):
    inter=ast.literal_eval(n.split("_")[3].replace(".tsv",""))
    df=pd.read_csv(f"blast2_inter_split/{n}.tsv",sep="\t", names="qseqid sseqid stitle staxids sscinames sphylums skingdoms pident length mismatch gapopen qstart qend sstart send evalue bitscore".split(" "))
    gene=";".join(n.split(";")[0:2])
    leng=len(record_dict[n.split('.tsv')[0]].seq)
    df["cov"]=(np.array(df.qend)-np.array(df.qstart)+1)/leng
    dfo=df[df["cov"]>.30]
    dfo=dfo[~dfo.sphylums.astype(str).str.contains("Arthropoda")]
    dfo=dfo[~dfo.sphylums.astype(str).str.contains("Rotifera")]
    dfo=dfo[dfo.staxids.astype(str)!="nan"]
    dfo=dfo[dfo.staxids!=32630]
    dfm=dfo.iloc[0:30000,:]
    dfmeta=dfm[dfm.skingdoms.astype(str).str.contains("Metazoa")]
    dfhgt=dfm[~dfm.skingdoms.astype(str).str.contains("Metazoa")]
    dfhgt["AI"]=np.log10(dfmeta.evalue.min()+1e-200)-np.log10(dfhgt.evalue+1e-200)
    dfmeta["MI"]=np.log10(dfhgt.evalue.min()+1e-200)-np.log10(dfmeta.evalue+1e-200)
    dfmi=dfm.iloc[0:300,:]
    dfmetai=dfmi[dfmi.skingdoms.astype(str).str.contains("Metazoa")]
    dfhgti=dfmi[~dfmi.skingdoms.astype(str).str.contains("Metazoa")]
    
    if dfm.shape[0]>0:
        if dfmeta.evalue.min()<.1  and (dfhgt.shape[0]==0 or len(set(dfmeta[dfmeta.MI>1].staxids))>5 or (len(set(dfmetai.staxids))/len(set(dfmi.staxids))>.40 and len(set(dfhgt[dfhgt.AI>5].staxids))<2)):
            return "Meta"
        elif dfhgt.evalue.min()<.1 and len(set(dfhgt.staxids))>10 and (dfmeta.shape[0]==0 or len(set(dfhgt[dfhgt.AI>5].staxids))>10 or (len(set(dfhgti.staxids))/len(set(dfmi.staxids))>.90 and len(set(dfmeta[dfmeta.MI>5].staxids))<2)) :
            return "HGT"
    return

record_dict=SeqIO.to_dict(SeqIO.parse('interval_sep_fasta', 'fasta'))
meta=[x.split(".tsv")[0] for x in os.listdir("blast2_inter_split") if "Meta" in x]
hgt=[x.split(".tsv")[0] for x in os.listdir("blast2_inter_split") if "HGT" in x]

#annotate putative HGT intervals and store confirmed ones
with mp.Pool(28) as p:
    hgts2 = p.map(check_annot, hgt)
mpi_hgt={x:y for x,y in zip(hgt,hgts2)}
hgt_set=set([x.split(";")[0]+";"+x.split(";")[1] for x in mpi_hgt if mpi_hgt[x]=="HGT"])

#annotate putative Meta intervals and store confirmed ones
with mp.Pool(28) as p:
    meta2 = p.map(check_annot, meta)
mpi_meta={x:y for x,y in zip(meta,meta2)}
meta_set=set([x.split(";")[0]+";"+x.split(";")[1] for x in mpi_meta if mpi_meta[x]=="Meta"])

#select chimeras: contain confirmed HGT and Meta intervals
fs90=meta_set&hgt_set

#write HGT intervals to output file
hgt_incl={x for x in mpi_hgt if x.split(";")[0]+";"+x.split(";")[1] in fs90}
f=open("hgt_incl.txt","w")
for x in hgt_incl:
    f.write(x)
    f.write("\n")
f.close()

#write Meta intervals to output file
hgt_incl={x for x in mpi_meta if x.split(";")[0]+";"+x.split(";")[1] in fs90}
f=open("meta_incl.txt","w")
for x in hgt_incl:
    f.write(x)
    f.write("\n")
f.close()