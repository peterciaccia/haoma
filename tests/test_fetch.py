"""
Created on 2021-09-21 by Peter Ciaccia
"""

import logging as log
from EntrezpyTools.entrezpy_tools import EntrezSession
import test_tools

test_tools.config_test_log(__file__)

# Test 1 - Fetches UIDs by passing kwargs to EntrezSession object
log.info('Test 1')
Test = EntrezSession()
log.debug('EntrezSession instantiated')
params = {
    'db': 'nucleotide',
    'term': 'viruses[orgn',
    'retmax': 3,
    'rettype': 'uilist'
}
output1 = Test.fetch_UIDs(**params)
log.debug(output1)
if output1 == ['2095581274', '2095581262', '2095581251']:
    log.info('Test 1 passed')
else:
    log.warning('Test 1 failed')


# Test 2 - Fetches UIDs by using default params
log.info('Test 2')
Test2 = EntrezSession()
log.debug('EntrezSession instantiated')
output2 = Test2.fetch_UIDs()
log.debug(output2)
if output2 == ['167']:
    log.info('Test 2 passed')
else:
    log.warning('Test 2 failed')

# Test 3 -

# Test.esearch_2()
# Test.efetch(uids)
