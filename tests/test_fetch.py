"""
Created on 2021-09-21 by Peter Ciaccia
"""

import logging as log
from EntrezpyTools.entrezpy_tools import EntrezSession
import test_tools

test_tools.config_test_log(__file__)

# Test 1 - Fetches UIDs by passing kwargs to EntrezSession object
# log.info('Test 1')
# Test = EntrezSession()
# log.debug('EntrezSession instantiated')
# params = {
#     'db': 'nucleotide',
#     'term': 'viruses[orgn',
#     'retmax': 3,
#     'rettype': 'uilist'
# }
# output1 = Test.fetch_UIDs(**params)
# log.debug(output1)

# Test 2 - Fetches UIDs by using default params
log.info('Test 2')
Test2 = EntrezSession()
log.debug('EntrezSession instantiated')
output2 = Test2.fetch_UIDs()
log.debug(output2)

# Test 3 -

# Test.esearch_2()
# Test.efetch(uids)
