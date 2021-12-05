"""
Created 2021-10-12
Connects to mysql container when imported
"""
import logging
import os
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
# from sqlalchemy.ext.automap import automap_base
# from library.refseq import RefSeq_to_Uniprot

logging.debug('Creating declarative base instance')
Base = declarative_base()



def stats(eng):
    """
    returns, prints Base.metadata
    :param eng:
    :return:
    """
    # metadata_obj = MetaData()
    # metadata_obj.reflect(bind=eng)
    # print([table.name for table in metadata_obj.sorted_tables])
    Base = declarative_base(bind=eng)
    pass
    # meta = uniprot.Base.metadata
    print(Base.metadata)
    return Base.metadata


def get_size(session, Table_Declaration, verbose=False):
    """
    Returns number of rows in Table
    :param session: sqlalchemy session
    :param Table_Declaration: Declarative table class (uninstantiated)
    :param verbose:
    :return:
    """
    num_rows = session.query(Table_Declaration).count()
    if verbose:
        print(f"Rows:\t{num_rows}")
    return num_rows
