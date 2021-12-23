"""
Created by Peter Ciaccia on 2021-10-27
Purpose: determine best chunk size for flat file import
Findings: Chunk size of 10,000 was faster than chunk size of 100,000
"""

# internal modules
import logging
import test_tools
# initial config needs to be defined for each test script
from db import engine
from db.models.models import RefSeq_to_Uniprot
from test_tools import timer

logging.basicConfig(filename=test_tools.get_log_path(),
                    filemode="w",
                    level=logging.DEBUG,
                    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    # force=True
                    )
logger = logging.getLogger(__name__)


def rebuild_table(chunk_size=10000, repopulate=True):
    chunks = RefSeq_to_Uniprot.parse(debug=True, chunk_size=chunk_size)
    RefSeq_to_Uniprot.populate(chunks, engine, debug=True, repopulate=repopulate)


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
    rebuild_table(*args, **kwargs, chunk_size=10000)



if __name__ == '__main__':
    run()
