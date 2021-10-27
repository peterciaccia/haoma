"""
Created by Peter Ciaccia on 2021-10-27
Debugs Uniprot IDMapping schema population
"""

from connect import engine
from library import uniprot


uniprot.Base.metadata.create_all(bind=engine)
uniprot.load_idmapping(engine, debug=True)
