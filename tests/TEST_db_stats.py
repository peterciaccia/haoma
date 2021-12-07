"""
Created by Peter Ciaccia on 2021-12-04
Purpose:
Findings:
"""

# external dependencies
from sqlalchemy.orm import sessionmaker

# in-app modules
import logging
import test_tools
# initial config needs to be defined for each test script
logging.basicConfig(filename=test_tools.get_log_path(),
                    filemode="w",
                    level=logging.DEBUG,
                    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    )
from db import connect
from db.models import refseq

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    connect.get_size(refseq.RefSeq_to_Uniprot, verbose=True)
