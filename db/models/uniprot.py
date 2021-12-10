"""
Created on 2021-10-12 by Peter Ciaccia
"""
import os

import pandas as pd
from sqlalchemy import Table, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db import Session, Base
from db.models.refseq import RefSeq_to_Uniprot


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
# uniprot_idmapping = [
#     "UniProtKB_AC",
#     "UniProtKB_ID",
#     "GeneID",
#     "RefSeq"
# ]

nested_ids = [
    'RefSeq',
    'GO',
    'PDB',
    'PIR',
    'MIM',
    'UniGene',
    'PubMed',
    'EMBL',
    'EMBL_CDS',
    'Ensembl',
    'Ensembl_TRS',
    'Ensembl_PRO',
    'Additional_PubMed',
]

class UniprotIdMap(Base):
    __tablename__ = 'uniprot_idmap'
    # __table_args__ = {'schema': 'haomalib'}

    UniProtKB_AC = Column('UniProtKB_AC', String(16), primary_key=True)
    UniProtKB_ID = Column('UniProtKB_ID', String(16))
    GeneID       = Column('GeneID', Integer)
    # RefSeq = Column("RefSeq", String(16))
    # RefSeq       = relationship("RefSeq",
    #                             # secondary=UniprotKB_AC_link_RefSeq,
    #                             backref='uniprot_idmap',
    #                             cascade="all, delete"
    #                             )

    # GI           = relationship("GI", primaryjoin='UniprotIdMap.GI==UniprotGI.GI', backref='uniprot_idmap')
    # GO           = relationship("UniprotGO", backref='uniprot_idmap')
    # PDB          = relationship("UniprotPdb", backref='uniprot_idmap')
    UniRef100    = Column('UniRef100', String(24))
    UniRef90     = Column('UniRef90', String(24))
    UniRef50     = Column('UniRef50', String(24))
    UniParc      = Column('UniParc', String(16))
    # PIR          = relationship("UniprotPir", backref='uniprot_idmap')
    NCBI_taxon   = Column('NCBI_taxon', Integer())
    # MIM          = relationship("UniprotMim", backref='uniprot_idmap')
    # UniGene      = relationship("UniGene", backref='uniprot_idmap')
    # PubMed       = relationship("Pubmed", backref='uniprot_idmap')
    # EMBL         = relationship("Embl")
    # EMBL_CDS     = relationship("Embl_Cds", backref='uniprot_idmap')
    # Ensembl      = relationship("Ensembl")
    # Ensembl_TRS  = relationship("EnsemblTrs", backref='uniprot_idmap')
    # Ensembl_PRO  = relationship("EnsemblPro", backref='uniprot_idmap')
    # Additional_PubMed = relationship("AddtlPubmed", backref='uniprot_idmap')

    def __repr__(self):
        return f"UniprotIdMap(" \
               f"UniProtKB_AC={self.UniProtKB_AC!r}, " \
               f"UniProtKB_ID={self.UniProtKB_ID!r}, " \
               f"GeneID={self.GeneID!r}, " \
               f"RefSeq={self.RefSeq!r})"


class UniprotIdmappingBase(Base):
    __abstract__ = True
    # id = Column(String(24), primary_key=True)

    # @declared_attr
    # def UniProtKB_AC(cls):
    #     return Column(String(16), ForeignKey('uniprot_idmap.UniProtKB_AC'))


# class RefSeq(UniprotIdmappingBase):
#     __tablename__ = 'refseq'
#     refseq = Column(String(16), primary_key=True)
#     UniProtKB_AC = relationship("UniProtKB_AC", secondary=UniprotKB_AC_link_RefSeq)


# class UniprotKB_AC_link_RefSeq(Base):
#     __tablename__ = 'Uniprot2RefSeq'

    # UniprotKB_AC = Column(String(16), ForeignKey(UniprotIdMap.UniProtKB_AC), primary_key=True)
    # RefSeq = Column(String(16), ForeignKey(RefSeq_to_Uniprot.RefSeq_id), primary_key=True)

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

def _split_multiple(UniProtKB_AC, nested_id_str):
    rows = [UniprotIdMap(UniProtKB_AC=UniProtKB_AC, RefSeq=refSeq)
            for refSeq in nested_id_str.split('; ')
            ]
    return rows


def _expand_nested_id_rows(df):
    for col in nested_ids:
        rows = [row for sublist in
                [_split_multiple(x, y) for x, y in zip(df['UniProtKB_AC'], df[col])]
                for row in sublist]
        for row in rows:
            print(row)


def parse(chunksize=100000, debug=False):

    if debug:
        filename = "idmapping.debug_03.txt"
    else:
        raise NotImplementedError("A local copy is not stored; may be better to store remotely")
    data_path = os.path.join(os.getenv('EXTERNAL_DATA_DIR'),'uniprot/knowledgebase/idmapping/', filename)
    reader = pd.read_csv(data_path,
                         chunksize=chunksize,
                         delimiter='\t',
                         names=uniprot_idmapping,
                         keep_default_na=False
                         )
    for df in reader:
        _expand_nested_id_rows(df)
