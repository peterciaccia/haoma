"""
This script is for testing various components of app.py
"""

import logging as log
import os

import parts
import test_tools
import app

test_tools.config_test_log(__file__)

Importer = app.ImportWizardDev()
Importer.import_seq('P_tetR.fa')
Importer.import_seq('eyfp.fa')
Importer.import_seq('L3S2P21.fa')
myrecords = Importer.get_records()

recipe1 = [myrecords[x] for x in ['P_tetR', 'eyfp', 'L3S2P21']]


Promoter = parts.Promoter
cds_instance = parts.Cds(myrecords['eYFP'])
Cds = parts.Cds
Terminator = parts.Terminator
partschema = (Promoter, Cds, Terminator)

schema = parts.PartSchema(partschema, app.System('Escherichia coli'))
seq = schema.get_draft_sequence(recipe1)
print(seq)
# PartLibrary.PartInterface()
