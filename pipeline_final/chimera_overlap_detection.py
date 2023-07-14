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

record_dict = SeqIO.to_dict(SeqIO.parse('scaffold_genomes/ncbi_dataset/data/combined_output.fa', 'fasta'))
a=open("all_interval_results.txt","r").readlines()
a=[ai.replace("\n","") for ai in a]

#parse the interval annotations and store in a dictionary key=query, value=lst of interval tuples 
result = {}
for item in a:
    parts = item.split(":", 1)

    key = parts[0]

    values = item.replace(key+":","").split("', ")

    new_value = {}
    if len(values)>=1 and values[0]!="[]":

        for v in values:

            v_parts = v.replace('"',"").replace("[","").replace("]","").replace("'","").split(":")
            new_value[ast.literal_eval(v_parts[1])] = v_parts[0]
        result[key] = new_value

#determine putatitive chimeras as sequences w/ at least 1 meta AND HGT interval         
def is_chimera(ai):
    if "HGT" in ai and "Meta" in ai:
        return ai
with mp.Pool(10) as p:
    chimera_candidates = p.map(is_chimera,a) 
cc=[x for x in chimera_candidates if x!=None]
cc=[x.split(":")[0] for x in cc]
results1={x:result[x] for x in cc}



#returns all sseqids in a blast output dataframe overlapping with an interval (tuple), with percentage length cutoff f (float)
def get_overlapping_sseqids(interval, dataframe,filtered=False,f=.30):
    start, end = interval

    # Filter rows where qend is greater than start and qstart is less than end
    filtered_df = dataframe[(dataframe['qend'] > start) & (dataframe['qstart'] < end)].sort_values("evalue")
#     print(Counter(list(filtered_df.skingdoms)))
    tot=filtered_df.shape[0]
    if filtered:
        filtered_df=filtered_df.iloc[0:50,:]

    # Calculate the length of the interval
    interval_length = end - start

    # Calculate the minimum overlap length required (30% of the interval length)
    min_overlap_length = f * interval_length

    # Filter rows where the overlap length is greater than or equal to the minimum required
    overlapping_df = filtered_df[filtered_df['qend'] - filtered_df['qstart'] >= min_overlap_length]

    # Return the sseqid values of the overlapping rows
    overlapping_sseqids = overlapping_df['sseqid'].tolist()

    return overlapping_sseqids,tot

#checks to ensure that the maximum number of overlapping sequences between any meta and HGT interval<5
def check_overlaps(n):
    df=pd.read_csv(f"inter_blast_result/{n}.tsv",sep="\t", names="qseqid sseqid stitle staxids sscinames sphylums skingdoms pident length mismatch gapopen qstart qend sstart send evalue bitscore".split(" "), dtype={"staxids": str})
    df=df[~df.sphylums.astype(str).str.contains("Arthropoda")]
    df=df[df.staxids.astype(str)!="nan"]
    df=df.sort_values("evalue").iloc[0:int(2e4),:]
    m=result[n]
 
    m2={}
    for n1 in m:
        
     
        if m[n1]=="HGT":
            
            hgto,tothgt=get_overlapping_sseqids(n1,df,True)
            
            overlaps=[]
            for n2 in m:
   
                if m[n2]=="Meta":
                    meto,tot=get_overlapping_sseqids(n2,df)
                  
                    overlaps.append(len(set(meto)&set(hgto)))
            if max(overlaps)<5:
                m2[n1]=m[n1]
        else:
            meto,totmet=get_overlapping_sseqids(n1,df,True)
           
            overlaps=[]
            for n2 in m:
                if m[n2]=="HGT":
                    hgto,tothght=get_overlapping_sseqids(n2,df)
                    overlaps.append(len(set(meto)&set(hgto)))                    
            if max(overlaps)<5:
                m2[n1]=m[n1]
            
    return m2

with mp.Pool(20) as p:
    chimera_candidates = p.map(check_overlaps,list(results1.keys())) 
results2o={x:y for x,y in zip(list(results1.keys()),chimera_candidates) }
results2={x:results2o[x] for x in results2o if "HGT" in str(results2o[x]) and "Meta" in str(results2o[x]) }


#makes sure that a full length (>90% coverage) blast hit is in arthropoda but not outside arthropoda
def tot_overlap(n):

    l=len(record_dict[n].seq)
    df=pd.read_csv(f"inter_blast_result/{n}.tsv",sep="\t", names="qseqid sseqid stitle staxids sscinames sphylums skingdoms pident length mismatch gapopen qstart qend sstart send evalue bitscore".split(" "), dtype={"staxids": str})
    df=df[~df.sphylums.astype(str).str.contains("Rotifera")]
    df=df[df.staxids.astype(str)!="nan"]
    df=df[df.staxids!=32630]
    df=df[df.evalue<1]
    art=df[df.sphylums.astype(str).str.contains("Arthropoda")]
    art_l=n.split(";")[1] in list(art.sseqid) or len(get_overlapping_sseqids((1,l), art,False,.90)[0])>0
    
    no_art=df[~df.sphylums.astype(str).str.contains("Arthropoda")]
    no_art_l=len(get_overlapping_sseqids((1,l), no_art,False,.90)[0])<2
    
    return art_l and no_art_l

with mp.Pool(20) as p:
    chimera_candidates = p.map(tot_overlap,list(results2.keys())) 
results3o={x:y for x,y in zip(list(results2.keys()),chimera_candidates) }
results3={x:results2[x] for x in results2 if  results3o[x]==True }

import pickle
with open('inter_scan_blast.pickle', 'wb') as handle:
    pickle.dump(results3, handle, protocol=pickle.HIGHEST_PROTOCOL)