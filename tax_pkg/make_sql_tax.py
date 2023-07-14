import pandas as pd
from sqlalchemy import create_engine
import os
os.chdir("/n/holyscratch01/extavour_lab/Lab/rkapoor/dbs")
csv_database = create_engine('sqlite:///accession2taxid', echo=False)
for df in pd.read_csv('accession2taxid.csv',sep="\t", chunksize=1000000,index_col="accession.version"):
    df = df.rename(columns={c: c.replace(' ', '') for c in df.columns})
    df.to_sql('FACT', csv_database, if_exists='append')