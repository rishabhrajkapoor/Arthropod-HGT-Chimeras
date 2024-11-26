import subprocess
from ete3 import Tree
import os
import sys
os.chdir(sys.argv[1])
subprocess.run(["python3", "/n/holylabs/LABS/extavour_lab/Users/rkapoor/pipeline_final/MAD/mad.py", "rev_aa.treefile" ,"-n"]) 
tbs=Tree("rev_aa.treefile")
trs=Tree("rev_aa.treefile.rooted")

for n in trs.iter_descendants("preorder"):
    l =[ str(leaf) for leaf in n]
    l2=[x.split("--")[1] for x in l]
    break
if len(l2)>1:
    tbs.set_outgroup(tbs.get_common_ancestor(l2))
else:
    tbs.set_outgroup(l2[0])
tbs.write(outfile="rev_aa.treefile.rooted2")
