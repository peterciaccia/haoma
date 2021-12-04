"""
Created on 2021-10-12 by Peter Ciaccia
"""
import os

import pandas as pd
from sqlalchemy import Table, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base, declared_attr


Base = declarative_base()

uniprot_idmapping_path = "external_data/uniprot/knowledgebase/idmapping/README.txt"
uniprot_idmapping = [
    "UniProtKB_AC",
    "UniProtKB_ID",
    "GeneID", # (EntrezGene)
    "RefSeq",
    "GI",
    "PDB",
    "GO",
    "UniRef100",
    "UniRef90",
    "UniRef50",
    "UniParc",
    "PIR",
    "NCBI_taxon",
    "MIM",
    "UniGene",
    "PubMed",
    "EMBL",
    "EMBL_CDS",
    "Ensembl",
    "Ensembl_TRS",
    "Ensembl_PRO",
    "Additional_PubMed",
]
# TODO: Delete this after debugging
uniprot_idmapping = [
    "UniProtKB_AC",
    "UniProtKB_ID",
    "GeneID",
    "RefSeq"
]

association_table = Table('association', Base.metadata,
                          Column('UniProtKB_AC', ForeignKey('uniprot_idmap.UniProtKB_AC'), primary_key=True),
                          Column('RefSeq', ForeignKey('refseq.refseq'), primary_key=True)
)


class UniprotIdMap(Base):
    __tablename__ = 'uniprot_idmap'
    # __table_args__ = {'schema': 'haomalib'}

    UniProtKB_AC = Column('UniProtKB_AC', String(16), primary_key=True)
    UniProtKB_ID = Column('UniProtKB_ID', String(16))
    GeneID       = Column('GeneID', Integer)
    RefSeq       = relationship("RefSeq",
                                secondary=association_table,
                                backref='uniprot_idmap',
                                cascade="all, delete"
                                )

    # GI           = relationship("GI", primaryjoin='UniprotIdMap.GI==UniprotGI.GI', backref='uniprot_idmap')
    # GO           = relationship("UniprotGO", backref='uniprot_idmap')
    # PDB          = relationship("UniprotPdb", backref='uniprot_idmap')
    # UniRef100    = Column('UniRef100', String(24))
    # UniRef90     = Column('UniRef90', String(24))
    # UniRef50     = Column('UniRef50', String(24))
    # UniParc      = Column('UniParc', String(16))
    # PIR          = relationship("UniprotPir", backref='uniprot_idmap')
    # NCBI_taxon   = Column('NCBI_taxon', Integer())
    # MIM          = relationship("UniprotMim", backref='uniprot_idmap')
    # UniGene      = relationship("UniGene", backref='uniprot_idmap')
    # PubMed       = relationship("Pubmed", backref='uniprot_idmap')
    # EMBL         = relationship("Embl")
    # EMBL_CDS     = relationship("Embl_Cds", backref='uniprot_idmap')
    # Ensembl      = relationship("Ensembl")
    # Ensembl_TRS  = relationship("EnsemblTrs", backref='uniprot_idmap')
    # Ensembl_PRO  = relationship("EnsemblPro", backref='uniprot_idmap')
    # Additional_PubMed = relationship("AddtlPubmed", backref='uniprot_idmap')


class UniprotIdmappingBase(Base):
    __abstract__ = True
    # id = Column(String(24), primary_key=True)

    # @declared_attr
    # def UniProtKB_AC(cls):
    #     return Column(String(16), ForeignKey('uniprot_idmap.UniProtKB_AC'))


class RefSeq(UniprotIdmappingBase):
    __tablename__ = 'refseq'
    refseq = Column(String(16), primary_key=True)
    UniProtKB_AC = relationship("UniProtKB_AC", secondary=association_table)

"""
# TODO: Replace placeholder tables with foreign keys to other data sources
class UniprotGI(UniprotIdmappingBase):
    __tablename__ = 'uniprot_gi'
    GI = Column('GI', Integer, primary_key=True)


class UniprotPdb(UniprotIdmappingBase):
    __tablename__ = 'uniprot_pdb'
    Pdb = Column('PDB', String(8), primary_key=True)


class UniprotPir(UniprotIdmappingBase):
    __tablename__ = 'uniprot_pir'
    Pir = Column('PIR', String(8), primary_key=True)


class UniprotMim(UniprotIdmappingBase):
    __tablename__ = 'uniprot_mim'


class UniprotUniGene(UniprotIdmappingBase):
    __tablename__ = 'uniprot_unigene'


class UniprotPubmed(UniprotIdmappingBase):
    __tablename__ = 'uniprot_pubmed'


class UniprotEmbl(UniprotIdmappingBase):
    __tablename__ = 'uniprot_embl'


class UniprotEmblCds(UniprotIdmappingBase):
    __tablename__ = 'uniprot_emblcds'


class UniprotEnsembl(UniprotIdmappingBase):
    __tablename__ = 'uniprot_ensembl'


class UniprotEnsemblTrs(UniprotIdmappingBase):
    __tablename__ = 'uniprot_ensembltrs'


class UniprotEnsemblPro(UniprotIdmappingBase):
    __tablename__ = 'uniprot_ensemblpro'


class UniprotAddtlPubmed(UniprotIdmappingBase):
    __tablename__ = 'uniprot_additional_pubmed'


### Association table declarations

class AssociationBase(Base):
    __abstract__ = True

    @declared_attr
    def UniProtKB_AC(cls):
        return Column(String(255), ForeignKey('uniprot_idmap.UniProtKB_AC'), primary_key=True)


class AssociationGI(AssociationBase):
    __tablename__ = 'association_GI'
    GI = Column('GI', ForeignKey('uniprot_gi.GI'), primary_key=True)

class AssociationGO(AssociationBase):
    __tablename__ = 'uniprot_go'
    GO = Column('GO', ForeignKey('uniprot_gi.GO'), primary_key=True)

class AssociationPDB(AssociationBase):
    __tablename__ = 'pdb'
    pdb = Column('PDB', ForeignKey('uniprot_pdb.pdb'), primary_key=True)

class AssociationPIR(AssociationBase):
    __tablename__ = 'pir'
    pdb = Column('PIR', ForeignKey('uniprot_pdb.pir'), primary_key=True)

"""
################################################### Debugging



# .................
# Functions

def load_idmapping(debug=False):
    if debug:
        filename = "idmapping.debug_01.txt"
    else:
        raise NotImplementedError("A local copy is not stored; may be better to store remotely")
    data_path = os.path.join(os.getenv('EXTERNAL_DATA_DIR'), 'uniprot/knowledgebase/idmapping/', filename)
    df = pd.read_csv(data_path, delimiter='\t', names=uniprot_idmapping)

    print(df)