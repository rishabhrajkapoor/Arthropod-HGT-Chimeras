import pickle
import pandas as pd
import multiprocessing as mp
import numpy as np
import pickle
from Bio import SeqIO
import os
import subprocess
import sys
#written by RK with chatGPT


#load fasta w/ all queries 
record_dict = SeqIO.to_dict(SeqIO.parse('scaffold_genomes/ncbi_dataset/data/combined_output.fa', 'fasta'))

def get_overlapping_rows(df, x, N=False):
    """
    Returns a new DataFrame with all rows from the input DataFrame that overlap with the given position x.
    """
    overlapping_rows = df[(df['qstart'] <= x) & (df['qend'] >= x)]
    if N:
        return overlapping_rows.shape[0]
    return overlapping_rows


def count_overlapping_seqs(df, start, end):
    """
    Input: a df with blast hits and start, end coordinates for the length of the query 
    Returns an array of positions and an array of the number of overlapping blast hits for each position
    """
    # Create an interval index from the qstart and qend columns
    intervals = pd.IntervalIndex.from_arrays(df['qstart'], df['qend'], closed='both')
    
    # Create a Boolean index of intervals that overlap with the start and end positions
    mask = intervals.overlaps(pd.Interval(start, end, closed='both'))
    
    # Use the Boolean index to select the overlapping intervals and count the number of occurrences
    counts = intervals[mask].value_counts(sort=False)
    
    # Create a Series of counts for each position between the start and end
    positions = np.arange(start, end)
    num_seqs = np.zeros_like(positions)
    for i, pos in enumerate(positions):
        for interval in counts.index:
            if pos in interval:
                num_seqs[i] += 1
    
    return positions, num_seqs

def max_y_x(x, y):
    """
    Returns the x value corresponding to the maximum y value in the given x and y arrays.
    """
    max_y_index = np.argmax(y)  # Find the index of the maximum y value
    return x[max_y_index]  # Return the x value at that index

def merge_intervals(d):
    """
    Merges intervals with overlap greater than 15% by replacing them with the interval with the greatest number of hits.
    Input:
    - d: a dictionary with keys (start, stop) and values number of hits
    Returns:
    - A new dictionary with merged intervals
    """
    merged_d = {}
    for (start1, stop1), num1 in d.items():
        # Compute length of current interval
        length1 = stop1 - start1 + 1
        
        # Check for overlaps with other intervals
        max_num = num1
        max_interval = (start1, stop1)
        for (start2, stop2), num2 in d.items():
            # Ignore the current interval
            if (start1, stop1) == (start2, stop2):
                continue
            
            # Compute length of other interval
            length2 = stop2 - start2 + 1
            
            # Compute overlap between the intervals
            overlap = max(0, min(stop1, stop2) - max(start1, start2) + 1)
            
            # Compute the fraction of overlap with respect to the length of the current interval
            overlap_frac = overlap / length1
            
            # If the overlap is greater than 15% and the number associated with the other interval is greater,
            # update the maximum number and interval
            if overlap_frac > 0.15 and num2 > max_num:
                max_num = num2
                max_interval = (start2, stop2)
        
        # Add the maximum interval to the merged dictionary
        merged_d[max_interval] = max_num
    
    return merged_d

def find_peak_interval(pos,cov,dfi,f):
    """
    Input: array of positions, array of blast hit density by position, dataframe with blast hits, 
    threshold density cutoff (float) for intervals 
    
    Runs interval demarcation algorithm modified from Bréhélin et al. PLOS Computational Biology, 2018
    https://doi.org/10.1371/journal.pcbi.1005889
    
    """
    #identify global maximum in blast hit density and all seqs overlapping with it
    peak=max_y_x(pos,cov)
    unstable=False
    C=get_overlapping_rows(dfi,peak)
    
    #set preliminary interval boundaries
    Ce=max(dfi.qend)
    Cs=min(dfi.qstart)
    
    #trim interval boundaries until both ends have at least f*max (peak) density
    N=C.shape[0]
    Ns=get_overlapping_rows(C, Cs, True)
    Ne=get_overlapping_rows(C, Ce, True)
    Cei=Ce
    Csi=Cs
    if Ns<f*N:
        Cs+=1
        unstable=True
    if Ne<f*N:
        Ce-=1
        unstable=True
    while unstable:
        Ns=get_overlapping_rows(C, Cs, True)
        Ne=get_overlapping_rows(C, Ce, True)

        if Ns>=f*N and Ne>=f*N:
            break
        else:
            if Ns<f*N:
                Cs+=1

            if Ne<f*N:
                Ce-=1
   
    return (Cei, Csi),(Cs, Ce),C

def get_annots(nam):
    """
    Input: name of a df in inter_blast_results directory (for a single query)
    Runs interval demarcation algorithm then applies HGT ancestry annotation to each interval
    Writes all metazoan and HGT intervals to "all_interval_results_shared.txt" in name:interval list format
    
    """
    try:
        #load dataframe, select top 30000 hits by evalue excluding arthropod hits
        dfo=pd.read_csv(f"inter_blast_results/{nam}.tsv",sep="\t", names="qseqid sseqid stitle staxids sscinames sphylums skingdoms pident length mismatch gapopen qstart qend sstart send evalue bitscore".split(" "))
        dfo=dfo[~dfo.sphylums.astype(str).str.contains("Arthropoda")]
        df1=dfo.loc[:,["sseqid","qstart","qend","sstart","send"]]
        df1=df1.iloc[0:30000,:]
        
        #iteratively assign blast hits to intervals until <10 hits left
        dfi=df1.copy()
        intermd={}
        interm={}
        while dfi.shape[0]>10:
            #obtain blast hit coverage for all positions in query 
            ret=count_overlapping_seqs(dfi,0,len(record_dict[nam].seq))
            
            interi,inter,df=find_peak_interval(ret[0],ret[1],dfi,.20)
            if interi!=None:
                dfi=dfi.drop(df.index)
                #saves interval and its number of overlapping hits if length of interval>35 residues and overlapping hits>10
                if inter[1]-inter[0]>35 and df.shape[0]>10:
                    interm[inter]=df.shape[0]
                    intermd[inter]=df
        #merges intervals with overlapping hits            
        d=merge_intervals(interm)
        d=dict(sorted(d.items()))
        
        #annotates ancestry of each interval as Meta (ancient metazoan), HGT, or neither. 
        inters=[]
        for di in d:
            df=intermd[di]
            dfm=dfo.loc[df.index,:]
            dfm=dfm[~dfm.sphylums.astype(str).str.contains("Rotifera")]
            dfm=dfm[dfm.sphylums.astype(str)!="nan"]
            dfm=dfm[dfm.staxids!=32630]
            dfmeta=dfm[dfm.skingdoms.astype(str).str.contains("Metazoa")]
            dfhgt=dfm[~dfm.skingdoms.astype(str).str.contains("Metazoa")]
            dfhgt["AI"]=np.log10(dfmeta.evalue.min()+1e-200)-np.log10(dfhgt.evalue+1e-200)
            dfmeta["MI"]=np.log10(dfhgt.evalue.min()+1e-200)-np.log10(dfmeta.evalue+1e-200)
            dfmi=dfm.iloc[0:300,:]
            dfmetai=dfmi[dfmi.skingdoms.astype(str).str.contains("Metazoa")]
            dfhgti=dfmi[~dfmi.skingdoms.astype(str).str.contains("Metazoa")]
            if dfm.shape[0]>0:
                if dfhgt.shape[0]==0 or len(set(dfmeta[dfmeta.MI>1].staxids))>5 or (len(set(dfmetai.staxids))/len(set(dfmi.staxids))>.60 and len(set(dfhgt[dfhgt.AI>5].staxids))<2):
                    inters.append(f"Meta:{di}")
                elif dfmeta.shape[0]==0 or len(set(dfhgt[dfhgt.AI>5].staxids))>10 or (len(set(dfhgti.staxids))/len(set(dfmi.staxids))>.95 and len(set(dfmeta[dfmeta.MI>5].staxids))<2) :
                    inters.append(f"HGT:{di}")
        f=open("all_interval_results_shared.txt","a")
        f.write(f"{nam}:{str(inters)}")
        f.write("\n")
        f.close()
        return 
    except:
        f=open("all_interval_results_shared.txt","a")
        f.write(f"{nam}:FAIL")
        f.write("\n")
        f.close()
        return 

 