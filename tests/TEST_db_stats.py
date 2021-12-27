"""
Created by Peter Ciaccia on 2021-12-04
Purpose:
Findings:
"""

from test_tools import timer
import log.conf

from db import engine
from sqlalchemy import inspect
from sqlalchemy.ext.automap import automap_base

########################################################################################################################
########################################################################################################################

logger = log.conf.get_logger(module='test')
@timer
def run(*args, **kwargs):
    """
    Write tests here
    :param task:
    :param args:
    :param kwargs:
    :return:
    """
    logger.debug(f'logging "{__file__}"')
    inspector = inspect(engine)
    print(inspector.get_table_names())
    base = automap_base()
    base.prepare(engine, reflect=True)

###############################

run()
