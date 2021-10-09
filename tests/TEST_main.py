"""
This script is for testing various components of main.py
"""

import logging as log
import os

import parts
import test_tools
import main

test_tools.config_test_log(__file__)

Importer = main.ImportWizardDev()
Importer.import_seq('P_tetR.fa')
Importer.import_seq('eyfp.fa')
Importer.import_seq('L3S2P21.fa')
myrecords = Importer.get_records()


Promoter = parts.Promoter
# Cds = parts.Cds(myrecords['eYFP'])
Cds = parts.Cds
Terminator = parts.Terminator
partschema = (Promoter, Cds, Terminator)

schema = main.PartSchema(partschema, main.System('Escherichia coli'))

parts.PartInterface()
