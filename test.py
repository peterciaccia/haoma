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

# TODO: add all subdirectories function
project_tests_dir = os.getenv('PROJECT_TESTS_DIR')
sys.path.append(project_tests_dir)
# sys.path.append(os.path.join)


if __name__ == '__main__':
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = conf.get_logger(__name__)
    try:
        for test in sys.argv[1:]:
            logger.info(f'Running test {test}')
            importlib.import_module(test)
    except IndexError:
        'Ensure that the configuration includes a test script name (exclude .py)'
        raise
