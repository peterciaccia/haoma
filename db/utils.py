"""
Created 2021-10-12
Connects to mysql container when imported
"""
from db import Session, Base

import log.conf
logger = log.conf.get_logger(module='test')


# class SessionWrapper(Session):
#     # TODO wrap Session to handle exceptions
#     pass


# TODO: wrong implementation; need automap_base
def stats(eng):
    """
    returns, prints Base.metadata
    :param eng:
    :return:
    """
    # metadata_obj = MetaData()
    # metadata_obj.reflect(bind=eng)
    # print([table.name for table in metadata_obj.sorted_tables])
    pass
    # meta = uniprot.Base.metadata
    print(Base.metadata)
    return Base.metadata


def get_size(Table_Declaration, log=True):
    """
    Returns number of rows in Table
    :param Table_Declaration: Declarative table class (uninstantiated)
    :param log:
    :return:
    """

    with Session() as s:
        nrows = s.query(Table_Declaration).count()
    if log:
        logger.debug(f"Table '{Table_Declaration.__tablename__}' contains {nrows} rows")
    return nrows


class LibraryViewer(object):

    def __init__(self):

        pass
        """
        Functionalities
        - list all table names
        - list all table names with number of entries
        -
        Considerations/Constraints
        - is making sure there's no open session necessary?
        - 
        """

    def get_metadata(self):

        pass
