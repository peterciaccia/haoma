


import pandas as pd
from sqlalchemy import Table, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base, declared_attr
import os


Base = declarative_base()


class RefSeq(Base):
    __tablename__ = 'refseq_to_uniprot'

    RefSeq = Column('RefSeq', String(16), primary_key=True)
    UniProtKB_AC = Column('UniProtKB_AC', String(16), primary_key=True)


def load(debug=False):
    if debug:
        path_from_data_root = "ncbi/refseq/uniprotkb/gene_refseq_uniprotkb_collab"
    else:
        raise NotImplementedError("A local copy is not stored; may be better to store remotely")
    data_path = os.path.join(os.getenv('EXTERNAL_DATA_DIR'), path_from_data_root)
    df = pd.read_csv(data_path, delimiter='\t', names=["RefSeq", "UniProtKB_AC"])
    print(df.size)
