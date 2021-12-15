"""
Created by Peter Ciaccia on 2021-10-27
Purpose: determine best chunk size for flat file import
Findings: Chunk size of 10,000 was faster than chunk size of 100,000
"""

import time

# internal modules
import logging
import test_tools
# initial config needs to be defined for each test script
logging.basicConfig(filename=test_tools.get_log_path(),
                    filemode="w",
                    level=logging.DEBUG,
                    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    # force=True
                    )
logger = logging.getLogger(__name__)
from db import engine
from db.models.models import RefSeq_to_Uniprot


def time_table_make(chunksize):
    chunklist = RefSeq_to_Uniprot.read(debug=True, chunksize=chunksize)
    RefSeq_to_Uniprot.populate(chunklist, engine, debug=True, repopulate=True)


def chunk_timer():
    chunksize_list = [
        10000,
        100000,
    ]

    for chunksize in chunksize_list:
        logger.info(f'timing chunksize = {chunksize}')
        starttime = time.time()

        time_table_make(chunksize=chunksize)
        endtime = time.time()
        elapsed = endtime - starttime
        logger.debug(f'elapsed time for chunksize {chunksize}: {elapsed:.8f}')

if __name__ == '__main__':
    time_table_make(chunksize=10000)
