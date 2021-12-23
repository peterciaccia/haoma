"""
Created by Peter Ciaccia on 2021-12-04
Purpose:
Findings:
"""


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
from db import utils, engine
from db.models import refseq

from sqlalchemy import inspect
from sqlalchemy.ext.automap import automap_base

logger = logging.getLogger(__name__)



inspector = inspect(engine)
print(inspector.get_table_names())


Base = automap_base()
Base.prepare(engine, reflect=True)


if __name__ == '__main__':
    # TODO: Implement this test
    # utils.get_size(refseq.RefSeq_to_Uniprot, verbose=True)
    pass