"""

"""
# built-ins
import logging
import logging.config

# dependencies
from dotenv import load_dotenv

# in-app
import os
from datetime import datetime
from pathlib import Path

load_dotenv()


def get_log_path():
    """
    Writes logs for most files except tests
    :return:
    """
    log_dir = Path(os.getenv('PROJECT_LOG_DIR'))
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_name = Path(now)
    log_path = log_dir / log_name.with_suffix('.log')
    return log_path


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s, %(levelname)-2s [%(name)s] %(module)s %(lineno)d:  %(message)s'
        },
    },
    'handlers': {
        'default': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'filename': get_log_path(),
            'mode': 'a',
            'encoding': 'utf-8'
        }
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True
        },
        'test': {
            'handlers': ['default', 'file'],
            'level': 'DEBUG',
            'propagate': True
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}


def resolve_class_namespace(cls):
    """Resolves namespace for logger"""
    return f"{cls.__module__}.{cls.__qualname__}"


def get_logger(module=None, cls=None):
    """Prepares logger for given class or module """
    if module is not None and cls is not None:
        raise ValueError('cannot pass module names and class declarations simultaneously')
    elif module is not None:
        logger = logging.getLogger(module)
    elif cls is not None:
        logger = logging.getLogger(resolve_class_namespace(cls))
    elif cls is None and module is None:
        logger = logging.getLogger()
        logger.debug('logger set to default root logger')
    else:
        raise SyntaxError

    return logger
