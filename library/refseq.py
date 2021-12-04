"""
created by Peter Ciaccia on 10/28/21
"""
import pandas as pd
from sqlalchemy import Table, Column, String, ForeignKey, insert, update
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import insert, dialect
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.orm import sessionmaker
import os

from library.connect import Base
from log import log_utils
logger = log_utils.get_logger(module=__name__)

# pandas options
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

class RefSeq(Base, DeferredReflection):
    __tablename__ = 'refseq_to_uniprot'

    RefSeq_id = Column('RefSeq_id', String(16), primary_key=True)
    UniProtKB_AC = Column('UniProtKB_AC', String(16), primary_key=True)

    def __repr__(self):
        return f"RefSeq(RefSeq_id={self.RefSeq_id!r}, UniProtKB_AC={self.UniProtKB_AC!r}"


def read(debug=False, chunksize=None):
    default_chunksize = 10000
    nrows = 2500000
    path_from_data_root = "ncbi/refseq/uniprotkb/gene_refseq_uniprotkb_collab"
    if debug:
        if chunksize is not None:
            logger.debug(f'chunk size set to {chunksize}')

        else:
            logger.debug(f'No chunk size specified; using default value {default_chunksize}')
            chunksize = default_chunksize
    else:
        nrows = None
        raise NotImplementedError()

    data_path = os.path.join(os.getenv('EXTERNAL_DATA_DIR'), path_from_data_root)
    chunks = []
    for chunk in pd.read_csv(
            data_path,
            delimiter='\t',
            names=["RefSeq", "UniProtKB_AC"],
            skiprows=1,
            chunksize=chunksize,
            nrows=nrows
    ):
        chunks.append(chunk)

    logger.debug(f'refseq table read into {len(chunks)} chunks')
    return chunks



def get_size(session, verbose=False):
    num_rows = session.query(RefSeq).count()
    if verbose:
        print(f"Rows:\t{num_rows}")
    return num_rows

def repopulate(chunklist, eng, debug=False, repopulate=False):

    # stmt_list = [insert(RefSeq).values(RefSeq_id=row['RefSeq'], UniProtKB_AC=row['UniProtKB_AC'])
    #                 .returning(RefSeq.RefSeq_id)
    #                 .compile(dialect=dialect())
    #             for i, row in df.iterrows()
    #             ]
    # obj_list = [RefSeq(RefSeq_id=row['RefSeq'], UniProtKB_AC=row['UniProtKB_AC'])
    #            for i, row in df.iterrows()
    #            ]
    # gets table name

    to_deletes = [RefSeq.__table__]
    Base.metadata.drop_all(bind=eng, tables=to_deletes)

    # gets table name
    tab = RefSeq.__table__
    print(tab)
    Base.metadata.create_all(bind=eng, checkfirst=True)
    DeferredReflection.prepare(eng)
    Session = sessionmaker(bind=eng)
    s = Session()
    get_size(s, verbose=True)
    for df in chunklist:
        rows = [RefSeq(RefSeq_id=row['RefSeq'], UniProtKB_AC=row['UniProtKB_AC']) for i, row in df.iterrows()]
        s.add_all(rows)
        s.commit()

    # for i, row in df.iterrows():
    #     stmt = insert(RefSeq).values(RefSeq_id=row['RefSeq'], UniProtKB_AC=row['UniProtKB_AC'])\
    #         .returning(RefSeq.RefSeq_id)\
    #         .compile(dialect=dialect())
    #     obj = RefSeq(RefSeq_id=row['RefSeq'], UniProtKB_AC=row['UniProtKB_AC'])
    #
    #     try:
    #         s.execute(stmt)
    #     except:
    #         logging.debug(f'[gene_refseq_uniprotkb_collab] Commit failed for row {obj.RefSeq_id}\t{obj.UniProtKB_AC}')
    #         s.rollback()
    #     finally:
    #         logging.debug('Session closing...')
    #         s.close()
    #         logging.debug('Session closed')




    # rows = s.query(RefSeq).count()
    # print(f'DB rows:\t{rows}')
    # print(f'# Objects:\t{len(obj_list)}')
    #
    # try:
    #     # for each in posts.query.filter(posts.id.in_(my_new_posts.keys())).all():
    #     # for row in s.query.filter(RefSeq.)
    #     #     s.add_all(objects_list)
    #     #     s.commit()
    #         s.execute(stmt)
    # except:
    #     logging.debug('Error in commit')
    #     s.rollback()
    #     raise
    # finally:
    #     logging.debug('Session closing...')
    #     s.close()
    #     logging.debug('Session closed')
