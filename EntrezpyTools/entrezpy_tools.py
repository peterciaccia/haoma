"""
Created 2021-09-21 by Peter Ciaccia
Contains classes, functions for geo-browser ipynb
"""

import os
from entrezpy import conduit
from entrezpy.esearch import esearcher


# ......................................................................................................................

class EntrezSession(object):
    def __init__(self):
        self.email = os.getenv('dev_email')
        self._ncbi_api_key = os.getenv('ncbi_api_key')
        self.c = conduit.Conduit(self.email)
        self.fetch_pipeline = self.c.new_pipeline()

    ### Example
    # c = conduit.Conduit('email')
    # fetch_pipeline = c.new_pipeline()
    #
    # sid = fetch_pipeline.add_search({'db': 'nucleotide',
    #                                  'term': 'viruses[organism]',
    #                                  'rettype': 'count'
    #                                  })
    # fetch_pipeline.add_fetch({'retmode': 'text',
    #                           'rettype': 'fasta'
    #                           }, dependency=sid
    #                          )
    #
    # c.run(fetch_pipeline)

    ######################################################
    # Esearch returning UIDs
    def fetch_UIDs(self, db='nucleotide',  term='viruses[orgn]', retmax=3, rettype='uilist', verbose=False):

        e = esearcher.Esearcher('esearcher', self.email)

        a = e.inquire({'db':db,
                       'term': term,
                       'retmax': retmax,
                       'rettype': rettype
                       })
        """
        'idtype' : 'acc'
        """
        uids = a.get_result().uids
        if verbose:
            print(uids)
        return uids

    def fetch_something(self):
        e = esearcher.Esearcher("entrezpy",
                                self.email,
                                apikey=self._ncbi_api_key,
                                apikey_var=os.getenv('ncbi_api_key'),
                                threads=None,
                                qid=None
                                )
        analyzer = e.inquire({'db': 'pubmed',
                              'term': 'viruses[orgn]',
                              'retmax': '20',
                              'rettype': 'uilist'})
        print(analyzer.result.count, analyzer.result.uids)
