"""
Created by Peter Ciaccia on 2021-10-27
Purpose: determine best chunk size for flat file import
Findings: Chunk size of 10,000 was faster than chunk size of 100,000
"""

# in-app; used for each test unless otherwise specific
import log.conf
from test_tools import timer

# in-app; test-specific
from db.models.sgd import SgdFeature
from db import engine

logger = log.conf.get_logger(module='test')


def parse_Sgd_features():

    SgdFeature.populate(eng=engine, repopulate=True, debug=True)


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

    parse_Sgd_features()


run()
