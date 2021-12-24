"""
Created 2021-10-12
Connects to mysql container when imported
"""
import logging
from db import Session, Base



# class SessionWrapper(Session):
#     # TODO wrap Session to handle exceptions
#     pass


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


def get_size(Table_Declaration, verbose=False):
    """
    Returns number of rows in Table
    :param session: sqlalchemy session
    :param Table_Declaration: Declarative table class (uninstantiated)
    :param verbose:
    :return:
    """

    with Session() as s:
        num_rows = s.query(Table_Declaration).count()
    if verbose:
        print(f"Rows:\t{num_rows}")
    return num_rows


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