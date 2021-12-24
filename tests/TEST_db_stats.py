"""
Created by Peter Ciaccia on 2021-12-04
Purpose:
Findings:
"""

# in-app modules
from test_tools import timer
import log.conf
# initial config needs to be defined for each test script
# logging.basicConfig(filename=get_log_path(),
#                     filemode="w",
#                     level=logging.DEBUG,
#                     format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
#                     datefmt='%Y-%m-%d:%H:%M:%S',
#                     )

from db import engine
from sqlalchemy import inspect
from sqlalchemy.ext.automap import automap_base

########################################################################################################################
########################################################################################################################

logger = log.conf.get_logger(module='TEST_db_stats')
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

