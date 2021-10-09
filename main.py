"""
Created by Peter Ciaccia
"""
import os
from pathlib import Path
from Bio import SeqIO

from dotenv import load_dotenv
load_dotenv()

import test_tools
test_tools.config_log()

class Workspace(object):
    """
    A Workspace object captures all relevant information related  to the instance of organism you design.
    :param object:
    :return:
    """

    #TODO:

    def __init__(self):
        pass


class ImportWizard(object):
    pass

    # contains

    ### general ###
    # TODO: Import .fasta as Seq object

    ### Rna-seq ###
    # TODO: Import .fastq

class System:

    def __init__(self, name):
        self.name = name


class PartSchema:
    """
    Defines part architecture
    :param system: instance or declaration of System child class
    :param schema: tuple of Part objects
    """
    def __init__(self, schema, system, schema_id=None):

        # system defines the part environment, usually means an organism, e.g. E. coli MG1655
        if schema_id is None:
            self.schema_id = 1
        else:
            self.schema_id = schema_id

        self.schema = schema
        self.system = system

    def get_schema(self):
        return

        # TODO: Import schema IDs from directory ?

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
