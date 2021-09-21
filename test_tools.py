"""
Created on 2021-09-21 by Peter Ciaccia
Contains common functions used for several test scripts, like reading and writing methods
"""

import os
from pathlib import Path
import logging
from datetime import datetime


# Writes logs
def write_test_log(filename):
    print(__file__)
    test_script_path = Path(filename)
    test_dir = test_script_path.parent.absolute() / "logs"
    test_filestem = test_script_path.stem
    test_output_path = test_dir / Path(test_filestem).with_suffix(".logs")
    test_output_str = r'{}'.format(test_output_path)
    try:
        with open(test_output_path, 'w') as f:
            f.write(str(datetime.now()))
    except FileNotFoundError:
        logging.warning('Log files not properly referenced. Logs may be incomplete')
    logging.basicConfig(filename=test_output_path, filemode="w", level=logging.DEBUG)

if __name__ == '__main__':
    write_test_log(__file__)
