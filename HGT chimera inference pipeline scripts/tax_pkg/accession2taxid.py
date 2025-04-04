from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import sys, os 








        
def get_taxid(x):
    engine = create_engine('sqlite:////n/holyscratch01/extavour_lab/Lab/rkapoor/dbs/accession2taxid', echo =False)
    results=[]
    
    with engine.connect() as connection:
        meta = MetaData()
        tbs = Table(
           'FACT', meta, 
            Column('taxid', String),
           Column('accession.version', String,primary_key = True)
        )
        s=tbs.select().where(tbs.c["accession.version"]==x)
        result = connection.execute(s)

        for row in result:
            results.append(row.taxid)
    if len(results)>0:
        if len(results)>1 and 7227 in results:
            results=results.remove(7227)
        return results[0]
    else:
        x=x.split(".")[0]+"."+str(int(x.split(".")[1])+1)
        with engine.connect() as connection:
            meta = MetaData()
            tbs = Table(
               'FACT', meta, 
                Column('taxid', String),
               Column('accession.version', String,primary_key = True)
            )
            s=tbs.select().where(tbs.c["accession.version"]==x)
            result = connection.execute(s)

            for row in result:
                results.append(row.taxid)
        if len(results)>0:
            if len(results)>1 and 7227 in results:
                results=results.remove(7227)
            return results[0]
    