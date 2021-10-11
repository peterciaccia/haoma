"""

"""

import logging
import logging.config
import log.conf

CONFIG = {'level':'INFO', 'quiet':True, 'propagate':True}


def get_root():
    """Returns the module root"""
    return 'Haoma'


def resolve_class_namespace(cls):
    """Resolves namespace for logger"""
    return f"{cls.__module__}.{cls.__qualname__}"


def get_class_logger(cls):
    """Prepares logger for given class """
    logger = logging.getLogger(f"{cls.__module__}.{cls.__qualname__}")
    logger.propagate = CONFIG['propagate']
    if CONFIG['quiet'] is True:
        logger.addHandler(logging.NullHandler())
        return logger
    logging.config.dictConfig(log.conf.default_config)
    logger.setLevel(CONFIG['level'])
    return logger
