"""
Created by Peter Ciaccia on 2021-10-27
Purpose: determine best chunk size for flat file import
Findings: Chunk size of 10,000 was faster than chink size of 100,000
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
from db import engine, Session
from db.models import refseq



def chunk_timer():
    chunksize_list = [
        10000,
        100000,
    ]

    for size in chunksize_list:
        logger.info(f'timing chunksize = {size}')
        chunklist = refseq.read(debug=True, chunksize=size)
        starttime = time.time()
        refseq.repopulate(chunklist, engine, debug=True)
        endtime = time.time()
        elapsed = endtime-starttime
        logger.debug(f'elapsed time for chunksize {size}: {elapsed:.8f}')


if __name__ == '__main__':
    chunk_timer()
