"""
Created on 2021-09-21 by Peter Ciaccia
Contains common functions used for several test scripts, like reading and writing methods
"""

import os
from pathlib import Path
import logging
from datetime import datetime


# Writes logs
def config_test_log(filename, logging_level=logging.DEBUG):
    print(__file__)
    test_script_path = Path(filename)
    test_dir = test_script_path.parent.absolute() / "logs"
    test_filestem = test_script_path.stem
    test_output_path = test_dir / Path(test_filestem).with_suffix(".log")
    logging.basicConfig(filename=test_output_path,
                        filemode="w",
                        level=logging_level,
                        format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d:%H:%M:%S'
                        )
    logging.info(str(datetime.now()))
    return

if __name__ == '__main__':
    ImportWarning('Not calling from test script. Called by self')
    config_test_log(__file__)
