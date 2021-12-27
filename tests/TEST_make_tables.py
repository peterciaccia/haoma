"""
Created by Peter Ciaccia on 2021-10-27
Purpose: determine best chunk size for flat file import
Findings: Chunk size of 10,000 was faster than chunk size of 100,000
"""

# internal modules
from test_tools import timer
import log.conf
# initial config needs to be defined for each test script
from db import engine
from db.models.models import RefSeq_to_Uniprot

logger = log.conf.get_logger(module='test')


def make_table(chunk_size=10000, repopulate=True):

    chunks = RefSeq_to_Uniprot.parse(debug=True, chunk_size=chunk_size)
    RefSeq_to_Uniprot.populate(chunks, engine, debug=True, repopulate=repopulate)


def rebuild_table(chunk_size=10000, repopulate=True):
    chunks = RefSeq_to_Uniprot.parse(debug=True, chunk_size=chunk_size)
    RefSeq_to_Uniprot.populate(chunks, engine, debug=True, repopulate=repopulate)


##############################################################################
##############################################################################
@timer
def run(*args, **kwargs):
    """
    Write tests here
    :param task:
    :param args:
    :param kwargs:
    :return:
    """
    logger.debug(f'Running test {__file__}')
    rebuild_table(*args, **kwargs, chunk_size=10000)
    return


run()
