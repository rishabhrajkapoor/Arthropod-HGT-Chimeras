import pandas as pd

df2=pd.read_csv("/n/holyscratch01/extavour_lab/Lab/rkapoor/dbs/nodes.dmp",sep="\t",header=None)
df=pd.read_csv("/n/holyscratch01/extavour_lab/Lab/rkapoor/dbs/names.dmp",sep="\t",header=None)
df=df.set_index(0)
df2=df2.set_index(0)
def get_lineage(taxid,l):
    
    if taxid==1:
        return l
    else:
       
        d=df.loc[taxid,:]
        if pd.DataFrame(d).shape[0]!=7:
            d=d[d[6]=="scientific name"]
        
        t=df2.loc[taxid,2]
        if pd.DataFrame(d).shape[0]==7:
            l[df2.loc[taxid,4]]=d[2]
        else:
            l[df2.loc[taxid,4]]=d.loc[taxid,2]
        return get_lineage(t,l)
def get_superkingdom(taxid,l):
    if taxid not in df.index:
        return "None"
    
    
    return l["superkingdom"]
def get_phylum(taxid,l):
    if taxid not in df.index:
        return "None"
    
    if "phylum" in l.keys():
        return pd.Series(l["phylum"]).iloc[0]
    elif "clade" in l:
        return pd.Series(l["clade"]).iloc[0]
    else:
        return "None"
def get_kingdom(taxid,l):
    if taxid not in df.index:
        return "None"
    
    if "kingdom" in l.keys():
        return pd.Series(l["kingdom"]).iloc[0]
    elif "clade" in l:
        return pd.Series(l["clade"]).iloc[0]
    else:
        return "None"
def get_kingdom(taxid,l):
    if taxid not in df.index:
        return "None"
    
    if "kingdom" in l.keys():
        return pd.Series(l["kingdom"]).iloc[0]
    else:
        return "None"
def get_order(taxid,l):
    if taxid not in df.index:
        return "None"
    if "order" in l.keys():
        return pd.Series(l["order"]).iloc[0]
    else:
        return "None" 
def get_class(taxid,l):
    if taxid not in df.index:
        return "None"
    if "class" in l.keys():
        return pd.Series(l["class"]).iloc[0]
    else:
        return "None" 

def get_colors(taxid,l):
    if get_superkingdom(taxid,l)=="Bacteria":
        return "blue"
    elif get_superkingdom(taxid,l)=="Eukaryota":
        if get_kingdom(taxid,l)=="Fungi":
            return "brown"
        elif get_kingdom(taxid,l)=="Viridiplantae":
            return "green"
        elif get_kingdom(taxid,l)=="Sar":
            return "teal"
        elif get_kingdom(taxid,l)=="Metazoa":
            if get_phylum(taxid,l)=="Arthropoda":
                return "pink"
            else:
                return "orange"
        else:
            return "black"
        
def get_species(x,l):
    try:
        ls=l['species']
        if type(ls) is str:
            s=ls
        else:
            s=list(l['species'])[0]
    except:
        s=x

    return s