"""
Created on 2021-09-21 by Peter Ciaccia
"""

import logging
from EntrezpyTools.entrezpy_tools import EntrezSession
import test_tools

test_tools.write_test_log(__file__)

Test = EntrezSession()
# logging.debug('EntrezSession instantiated')

uids = Test.fetch_UIDs(verbose=True)

Test.esearch_2()

Test.efetch(uids)

