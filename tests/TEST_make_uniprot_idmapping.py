"""
Created by Peter Ciaccia on 2021-10-27
Purpose: determine best chunk size for flat file import
Findings: Chunk size of 10,000 was faster than chunk size of 100,000.
Follow-up: Re-test using larger datasets
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

from db.models import uniprot

starttime = time.time()
uniprot.parse(debug=True)
endtime = time.time()
elapsed = endtime - starttime
print(elapsed)
