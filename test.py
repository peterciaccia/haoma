# built-ins
import os
import sys
import importlib
import logging.config
from log.conf import LOGGING_CONFIG

# dependencies
from dotenv import load_dotenv

# in-app
from log import conf

load_dotenv()
sys.path.append(os.getenv('PROJECT_TESTS_DIR'))

logger = conf.get_logger(__name__)

if __name__ == '__main__':
    logging.config.dictConfig(LOGGING_CONFIG)
    try:
        importlib.import_module(sys.argv[1])
    except IndexError:
        'Ensure that the configuration includes a test script name (exclude .py)'
        raise
