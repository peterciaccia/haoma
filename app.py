"""
Created by Peter Ciaccia
"""
import os
from pathlib import Path
from Bio import SeqIO

from dotenv import load_dotenv

import log.conf

load_dotenv()

import test_tools
log.conf.get_log_path()

class Workspace:
    """
    A Workspace object captures all relevant information related  to the instance of organism you design.
    :param object:
    :return:
    """

    #TODO:

    def __init__(self):
        pass


class ImportWizard:
    pass

    # contains

    ### general ###
    # TODO: Import .fasta as Seq object

    ### Rna-seq ###
    # TODO: Import .fastq

class System:

    def __init__(self, name):
        self.name = name


class NetworkSchema:
    """
    Defines network motifs for interacting parts
    """
    def __init__(self):
        pass

class PartBuilder:
    """
    PartBuilder assembles parts based on design schemas
    """
    def __init__(self):
        pass

####### temp classes
class ImportWizardDev:

    def __init__(self):
        self.records = {}

    def import_seq(self, file_, folder=os.getenv('PARTS_REPO'), filetype='fasta'):
        path = Path(folder).joinpath(file_)
        with open(path) as handle:
            for record in SeqIO.parse(handle, filetype):
                self.records[record.id] = record

    def get_records(self):
        return self.records

if __name__ == '__main__':
    Importer = ImportWizardDev()
    Importer.import_seq('P_tetR.fa')
    Importer.import_seq('tn10.gb', filetype='genbank')
    Importer.import_seq('tn10.gb')
    Importer.import_seq('L3S2P21.fa')
    myrecords = Importer.get_records()
    print(myrecords)
    # print(myrecords['AF162223.1'].seq)
