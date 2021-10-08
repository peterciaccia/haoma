"""
Created by Peter Ciaccia
"""
import os
from pathlib import Path
from Bio import SeqIO

from dotenv import load_dotenv
load_dotenv()


class Workspace(object):
    """
    A Workspace object captures all relevant information related  to the instance of organism you design.
    :param object:
    :return:
    """

    #TODO:


class ImportWizard(object):
    pass

    # contains

    ### general ###
    # TODO: Import .fasta as Seq object

    ### Rna-seq ###
    # TODO: Import .fastq

class _ImportWizard_dev:

    def __init__(self):
        folder = os.getenv('PARTS_REPO')



    def import_seq(self, file_, folder=os.getenv('PARTS_REPO')):
        path = Path(folder).joinpath(file_)
        with open(path) as handle:
            for record in SeqIO.parse(handle, "fasta"):
                print(record)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Importer = _ImportWizard_dev()
    Importer.import_seq('P_tetR.fa')