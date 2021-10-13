"""
Created on 2021-10-12 by Peter Ciaccia
"""

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base, declared_attr

Base = declarative_base()
uniprot_idmapping_path = "external_data/uniprot/knowledgebase/idmapping/README.txt"
uniprot_idmapping = [
    "UniProtKB-AC",
    "UniProtKB-ID",
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
    "NCBI-taxon",
    "MIM",
    "UniGene",
    "PubMed",
    "EMBL",
    "EMBL-CDS",
    "Ensembl",
    "Ensembl_TRS",
    "Ensembl_PRO",
    "Additional PubMed",
]

class UniprotIdMap(Base):
    __tablename__ = 'uniprot_idmap'
    # __table_args__ = {'mysql_engine':'InnoDB'}

    UniProtKB_AC = Column('UniProtKB_AC', String(255), primary_key=True)
    UniProtKB_ID = Column('UniProtKB_ID', String(255))
    GeneID       = Column('GeneID', Integer)
    RefSeq       = Column('RefSeq', String(255))
    GI           = relationship("Uniprot_GI", backref='uniprot_idmap')
    PDB          = relationship("UniprotPdb", backref='uniprot_idmap')
    GO           = relationship("UniprotGO", backref='uniprot_idmap')
    UniRef100    = Column('UniRef100', String(255))
    UniRef90     = Column('UniRef90', String(255))
    UniRef50     = Column('UniRef50', String(255))
    UniParc      = Column('UniParc', String(255))
    PIR          = relationship("UniprotPir", backref='uniprot_idmap')
    NCBI_taxon   = Column('NCBI_taxon', Integer())
    MIM          = relationship("UniprotMim", backref='uniprot_idmap')
    UniGene      = relationship("UniprotUniGene", backref='uniprot_idmap')
    PubMed       = relationship("UniprotPubmed", backref='uniprot_idmap')
    EMBL         = relationship("UniprotEmbl")
    EMBL_CDS     = relationship("UniprotEmblCds", backref='uniprot_idmap')
    Ensembl      = relationship("UniprotEnsembl")
    Ensembl_TRS  = relationship("UniprotEnsemblTrs", backref='uniprot_idmap')
    Ensembl_PRO  = relationship("UniprotEnsemblPro", backref='uniprot_idmap')
    Additional_PubMed = relationship("UniprotAddtlPubmed", backref='uniprot_idmap')

class UniprotIdmappingBase(Base):

    __abstract__ = True
    id = Column(String(), primary_key=True)

    @declared_attr
    def parent_id(cls):
        return Column(String(255), ForeignKey('UniprotIdMap.UniProtKB_AC'))


# TODO: Replace placeholder tables with foreign keys to other data sources

class UniprotGI(UniprotIdmappingBase):
    __tablename__ = 'uniprot-gi'

class UniprotGO(UniprotIdmappingBase):
    __tablename__ = 'uniprot-go'

class UniprotPdb(UniprotIdmappingBase):
    __tablename__ = 'uniprot-pdb'

class UniprotPir(UniprotIdmappingBase):
    __tablename__ = 'uniprot-pir'

class UniprotMim(UniprotIdmappingBase):
    __tablename__ = 'uniprot-mim'

class UniprotUniGene(UniprotIdmappingBase):
    __tablename__ = 'uniprot-unigene'

class UniprotPubmed(UniprotIdmappingBase):
    __tablename__ = 'uniprot-pubmed'

class UniprotEmbl(UniprotIdmappingBase):
    __tablename__ = 'uniprot-embl'

class UniprotEmblCds(UniprotIdmappingBase):
    __tablename__ = 'uniprot-emblcds'

class UniprotEnsembl(UniprotIdmappingBase):
    __tablename__ = 'uniprot-ensembl'

class UniprotEnsemblTrs(UniprotIdmappingBase):
    __tablename__ = 'uniprot-ensembltrs'

class UniprotEnsemblPro(UniprotIdmappingBase):
    __tablename__ = 'uniprot-ensemblpro'

class UniprotAddtlPubmed(UniprotIdmappingBase):
    __tablename__ = 'uniprot-additional-pubmed'

