

from EntrezpyTools.entrezpy_tools import EntrezSession

Test = EntrezSession()
uids = Test.fetch_UIDs(verbose=True)

Test.esearch_2()

Test.efetch(uids)