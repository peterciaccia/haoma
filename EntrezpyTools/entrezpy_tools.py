"""
Created 2021-09-21 by Peter Ciaccia
Contains classes, functions for geo-browser ipynb
"""

import os
from entrezpy import conduit
from entrezpy.esearch import esearcher
from entrezpy.efetch import efetcher
import logging as log


# ......................................................................................................................

class EntrezSession(object):
    def __init__(self):
        self.email = os.getenv('EMAIL')
        self.ncbi_api_key = os.getenv('NCBI_API_KEY')
        self.default_params = {
            'db': 'genome',
            'term': 'mg1655',
            'retmax': 3,
            'rettype': 'uilist'

        }
        self.params = {}
        self.params.update(self.default_params)
        pass

    # ..............................................................

    def set_params(self, params_update):
        """
        updates params attribute
        :param params_update:
        :return:
        """
        self.params.update(params_update)
        return

    # ..............................................................

    def get_params(self):
        """
        gets current params attribute
        :return:
        """
        return self.params

    # ..............................................................

    #
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
    # def fetch_UIDs(self, db='nucleotide',  term='viruses[orgn]', retmax=3, rettype='uilist', verbose=False):

    # ..............................................................

    def make_esearcher(self):

        e = esearcher.Esearcher('Haoma',
                                self.email,
                                apikey=self.ncbi_api_key,
                                qid=None
                                )

        return e

    def fetch_UIDs(self, **kwargs):
        """
        Sends Entrez request for UIDs based on passed parameters
        :param kwargs:
        :return: uids:
        """
        if kwargs == {}:
            self.set_params(self.default_params)
        else:
            self.set_params(kwargs)

        e = esearcher.Esearcher('Haoma',
                                self.email,
                                apikey=self.ncbi_api_key,
                                qid=None
                                )
        analyzer = e.inquire(self.get_params())

        uids = analyzer.get_result().uids
        return uids

    # ..............................................................

    def esearch_2(self):
        e = esearcher.Esearcher('Haoma',
                                self.email,
                                apikey=self.ncbi_api_key,
                                apikey_var=os.getenv('ncbi_api_key'),
                                threads=None,
                                qid=None
                                )
        analyzer = e.inquire({'db': 'pubmed',
                              'term': 'viruses[orgn]',
                              'retmax': '20',
                              'rettype': 'uilist'})
        print(analyzer.result.count, analyzer.result.uids)


# a list of uids is passed
    def efetch(self, uids):
        e = efetcher.Efetcher('Haoma',
                              self.email,
                              apikey=self.ncbi_api_key,
                              apikey_var=os.getenv('ncbi_api_key'),
                              threads=None,
                              qid=None
                              )
        analyzer = e.inquire({'db': 'pubmed',
                              'id': [17284678, 9997],
                              'retmode': 'text',
                              'rettype': 'abstract'})
        # print(analyzer.count, analyzer.retmax, analyzer.retstart, analyzer.uids)