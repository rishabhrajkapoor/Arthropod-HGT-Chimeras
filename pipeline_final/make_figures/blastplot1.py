import os
from pathlib import Path
import sys

import pandas as pd
import numpy as np   # numerical library
import subprocess

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import subprocess
import multiprocessing as mp
import ast
print("hi")

sys.path.insert(0, '/net/bos-nfsisilon/ifs/rc_labs/extavour_lab/rkapoor/home_migrate')
from tax_pkg import taxid
# from tax_pkg import accession2taxid
import pandas as pd
import multiprocessing as mp
import sys
import matplotlib.pyplot as plt

import matplotlib.font_manager
from matplotlib.font_manager import FontProperties

from pathlib import Path

import matplotlib as mpl
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

fig, ax = plt.subplots()

fpath = Path(mpl.get_data_path(), "/n/holylabs/LABS/extavour_lab/Users/rkapoor/envs/plot/fonts/arial.ttf")
from matplotlib.font_manager import FontProperties
from matplotlib import font_manager
plt.rcParams['figure.dpi'] = 300
font_path = "/n/holylabs/LABS/extavour_lab/Users/rkapoor/envs/plot/fonts/arial.ttf"
font_manager.fontManager.addfont("/n/holylabs/LABS/extavour_lab/Users/rkapoor/envs/plot/fonts/arial.ttf")
prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = prop.get_name()

import pickle
file_path = 'chimera_intervals_final.pickle'
with open(file_path, 'rb') as file:
    chimera_intervals=pickle.load(file)
genes=chimera_intervals.keys()
h_gene_intervals={}
meta_gene_intervals={}
results2={}
for x in genes:
    resultsa={}
    for xi in chimera_intervals[x]:
        if "HGT" in xi:
            resultsa[ast.literal_eval(xi.split("_")[-1])]="HGT"
        else:
            resultsa[ast.literal_eval(xi.split("_")[-1])]="Meta"
    results2[x]=resultsa

def get_color(ann):
    if "Viruses" in ann:
        return "yellow"
    if "Bacteria" in ann:
        return "blue"
    if "Fungi" in ann:
        return "brown"
    elif "Viridiplantae" in ann:
        return "green"
    elif "Arthropoda" in ann: 
        return "pink"
    elif "Metazoa" in ann:
        return "orange"
    else:
        return "black"
def get_taxid(ti):
    try:
        l=taxid.get_lineage(ti,{})
        sk=taxid.get_superkingdom(ti,l)
        k=taxid.get_kingdom(ti,l)
        p=taxid.get_phylum(ti,l)
        o=taxid.get_order(ti,l)
        c=get_color(str(l))
    except:
        ti="nan"
        return ("nan","nan","nan","nan","nan","nan")

    return (ti,sk,k,p,o,c)
lenmap={'XP_046664087.1': 585, 'XP_027204138.1': 987, 'XP_023346081.1': 261, 'XP_028168683.1': 471, 'XP_034487048.1': 586, 'XP_022243968.1': 1054, 'XP_046403459.1': 196, 'XP_046456339.1': 2163, 'XP_050528041.1': 793, 'XP_049785902.1': 564, 'XP_015833841.1': 1239, 'XP_031842795.1': 263, 'XP_033212818.1': 1241, 'XP_012275032.1': 1065, 'XP_037049533.1': 392, 'XP_037041958.1': 1320, 'XP_029821973.3': 979, 'XP_049849891.1': 642, 'XP_015786976.1': 1300, 'XP_026676798.1': 1946, 'XP_045595407.1': 576, 'XP_035711638.1': 1389, 'XP_021960153.2': 387, 'XP_035708240.1': 1023, 'XP_046646423.1': 1644, 'XP_026477151.1': 1735, 'XP_037026007.1': 395, 'XP_027199942.1': 708, 'XP_045779580.1': 706, 'XP_015834127.1': 551, 'XP_042220148.1': 591, 'XP_052563446.1': 475, 'XP_047736274.1': 709, 'XP_046453153.1': 869, 'XP_048512468.1': 1192, 'XP_046649021.1': 652, 'XP_036230923.1': 904, 'XP_035716531.1': 1078, 'XP_023329593.1': 646, 'XP_026318555.1': 524, 'XP_034233350.1': 315, 'XP_031340986.1': 881, 'XP_037790819.1': 1170, 'XP_035715441.1': 526, 'XP_049511280.1': 842, 'XP_002428156.1': 2081, 'XP_034827763.1': 1302, 'XP_035708168.1': 394, 'XP_037943392.1': 2323, 'XP_049849988.1': 834, 'XP_044731417.1': 881, 'XP_021958683.2': 294, 'XP_023332299.1': 400, 'XP_023318028.1': 1215, 'XP_045614234.1': 611, 'XP_046594669.1': 885, 'XP_040568466.1': 401, 'XP_040073766.1': 504, 'XP_051173821.1': 1137, 'XP_023328891.1': 391, 'XP_022178340.1': 1662, 'XP_046402901.1': 1335, 'XP_044763649.1': 774, 'XP_046439036.1': 824, 'XP_029662819.1': 340, 'XP_037030969.1': 299, 'XP_018903502.1': 866, 'XP_022173178.1': 973, 'XP_049881687.1': 432, 'XP_040564143.1': 931, 'XP_041972388.1': 1036, 'XP_042908388.1': 404, 'XP_044009448.1': 594, 'XP_036141434.1': 1845, 'XP_049881676.1': 633, 'XP_023324156.1': 799, 'XP_025018608.1': 372, 'XP_015837071.1': 537, 'XP_023236565.1': 672, 'XP_034245505.1': 549, 'XP_021699539.1': 1181, 'XP_014216391.1': 549, 'XP_035715507.1': 249, 'XP_018326454.1': 1189, 'XP_033210401.1': 1767, 'XP_008551656.1': 963, 'XP_046456336.1': 1376, 'XP_046456333.1': 2566, 'XP_031781467.1': 377, 'XP_025421543.1': 339, 'XP_023327453.1': 797, 'XP_039283995.1': 982, 'XP_023247543.1': 1347, 'XP_033209845.1': 2189, 'XP_046645476.1': 2021, 'XP_046396626.1': 327, 'XP_033212670.1': 1681,'XP_037026007.1':395}

def make_plotf(n):
    fig,ax=plt.subplots(1,2,dpi=300,figsize=(8,4))
    add=[x for x in os.listdir('blast_round_one_data') if n in x][0]
    ints=results2[n]
    df=pd.read_csv(f"blast_round_one_data/{add}",sep="\t", dtype={"staxids": str})
    # df=df[~df.sphylums.astype(str).str.contains("Arthropoda")]
    df=df[~df.sphylums.astype(str).str.contains("Rotifera")]
    df=df.sort_values("evalue").iloc[0:int(2e4),:]
    td=[]
    for x in df.staxids:
        if ";" in str(x):
            td.append(float(x.split(";")[0]))
        else:
            td.append(float(x))
    with mp.Pool(29) as p:
       
        hgts = p.map(get_taxid, td)
    df.loc[:,["taxid","superkingdom","kingdom","phylum","order","color"]]=hgts
    d=df[df.color.astype(str)!="nan"]
    d=d[d.color.astype(str)!="None"]
    d["color"]=d["color"].fillna("black")

    
    floor=1e-200

    for index, row in d.iterrows():
        ax[0].hlines(np.log10(float(row["evalue"])+floor),float(row["qstart"]),float(row["qend"]),color=row["color"],linewidth=1)
    mn=ax[0].get_ylim()[0]-.10*(ax[0].get_ylim()[1]-ax[0].get_ylim()[0])
    for y in ints:
        if ints[y]=="HGT":
            color="purple"
        else:
            color="orange"
        ax[0].hlines(mn,y[0],y[1],color,linewidth=7.0)
    ax[0].set_xlim(-20,lenmap[n]+20)
    ax[0].set_xlabel("Position with respect to query (N-C)",font=fpath)
    ax[0].set_ylabel("Log10(E-value+1e-200)",font=fpath)
    ax[0].set_title("Blast Results with Arthropod Hits",font=fpath)
    
    
    
    df=pd.read_csv(f"blast_round_one_data/{add}",sep="\t", dtype={"staxids": str})
    df=df[~df.sphylums.astype(str).str.contains("Arthropoda")]
    df=df[~df.sphylums.astype(str).str.contains("Rotifera")]
    df=df.sort_values("evalue").iloc[0:int(2e4),:]
    td=[]
    for x in df.staxids:
        if ";" in str(x):
            td.append(float(x.split(";")[0]))
        else:
            td.append(float(x))
    with mp.Pool(29) as p:
       
        hgts = p.map(get_taxid, td)
    df.loc[:,["taxid","superkingdom","kingdom","phylum","order","color"]]=hgts
    d=df[df.color.astype(str)!="nan"]
    d=d[d.color.astype(str)!="None"]
    d["color"]=d["color"].fillna("black")

    floor=1e-200
    for index, row in d.iterrows():
        ax[1].hlines(np.log10(float(row["evalue"])+floor),float(row["qstart"]),float(row["qend"]),color=row["color"],linewidth=1)
    mn=ax[1].get_ylim()[0]-.10*(ax[1].get_ylim()[1]-ax[1].get_ylim()[0])
    for y in ints:
        if ints[y]=="HGT":
            color="purple"
        else:
            color="orange"
        ax[1].hlines(mn,y[0],y[1],color,linewidth=7.0)
    ax[1].set_xlim(-20,lenmap[n]+20)
    ax[1].set_xlabel("Position with respect to query (N-C)",font=fpath)
    ax[1].set_title("Blast Results without Arthropod Hits",font=fpath)
    
    legend_elements = [Line2D([0], [0], color='yellow', lw=4, label='Viruses'),
                   Line2D([0], [0], color='blue', lw=4, label='Bacteria'),
                   Line2D([0], [0], color='brown', lw=4, label='Fungi'),
                   Line2D([0], [0], color='green', lw=4, label='Viridiplantae'),
                   Line2D([0], [0], color='orange', lw=4, label='Non-Arthropod Metazoa'),
                   Line2D([0], [0], color='pink', lw=4, label='Arthropoda'),
                   Line2D([0], [0], color='black', lw=4, label='Other')
                   ]

    custom_font = FontProperties(fname="/n/holylabs/LABS/extavour_lab/Users/rkapoor/envs/plot/fonts/arial.ttf", size=12)
    plt.legend(handles=legend_elements, bbox_to_anchor=(1.04, 1), loc="upper left", prop=custom_font)
    plt.savefig(f"blast_result_plots/{n}/round1_plot.svg",format="svg", bbox_inches="tight")
    plt.close(fig)

    return 

for n in genes:
    a=f"blast_result_plots/{n}"
    subprocess.run(["mkdir","-p",a])
    try:
        make_plotf(n)
    except:
        print(n)
