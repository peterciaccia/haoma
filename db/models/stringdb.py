# built-ins
import os
from pathlib import Path
import json

# dependencies
import pandas as pd
from sqlalchemy import Column, String, Integer, Float, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

# in-app
from db import engine
from db.Base import Base
from db import Session
from db.utils import get_size

import log.conf

logger = log.conf.get_logger(module='test')


class StringdbProteinLink(Base):
    __tablename__ = 'stringdb_protein_links'
    __table_args__ = {'extend_existing': True}
    data_relative_path = Path('external_data/string-db/by-organism/Saccharomyces-cerevisiae/'
                              '4932.protein.links.full.v11.5.txt.gz')

    def __repr__(self):
        return f"<StringdbProteinLink(protein_id={self.protein_id})>"

    @classmethod
    @property
    def table_drop_order(cls):
        return [
                # Add additional tables as needed here
                cls.__table__,
                ]

    @classmethod
    def parse(cls, debug=False):

        nrows = 1000 if debug else None
        for chunk in pd.read_csv(cls.data_path,
                                 compression='gzip',
                                 sep=' ',
                                 chunksize=100000,
                                 nrows=nrows):
            chunk.rename(columns={'protein1': 'protein_id', 'protein2': 'interacter_id'}, inplace=True)
            yield chunk

    @classmethod
    def populate(cls, eng=engine, repopulate=False, debug=False):

        # Table pre-formatting
        if repopulate:
            cls.drop_tables(checkfirst=False)
            logger.info(f"Dropped tables [{cls.__class__}]")
        Base.metadata.create_all(bind=eng, checkfirst=True)

        # Executes
        counter = 0
        for chunk in cls.parse(debug=debug):
            chunk.to_sql(cls.__tablename__, eng,
                         method='multi',
                         index=False,
                         if_exists='append')
            counter += 1
            logger.debug(f"Chunk {counter} added to {cls.__tablename__}")
            get_size(cls)

    protein_id = Column(String(16), primary_key=True)
    interacter_id = Column(String(16), primary_key=True)
    neighborhood = Column(Integer)
    neighborhood_transferred = Column(Integer)
    fusion = Column(Integer)
    cooccurence = Column(Integer)
    homology = Column(Integer)
    coexpression = Column(Integer)
    coexpression_transferred = Column(Integer)
    experiments = Column(Integer)
    experiments_transferred = Column(Integer)
    database = Column(Integer)
    database_transferred = Column(Integer)
    textmining = Column(Integer)
    textmining_transferred = Column(Integer)
    combined_score = Column(Integer)


class StringdbAlias(Base):
    __tablename__ = 'stringdb_protein_aliases'
    __table_args__ = {'extend_existing': True}
    data_relative_path = Path('external_data/string-db/by-organism/Saccharomyces-cerevisiae/'
                              '4932.protein.aliases.v11.5.txt.gz')
    # TODO: Make the below attributes abstract class attributes
    data_filename = Path(os.path.basename(data_relative_path))
    config_path = os.path.join(os.getenv('EXTERNAL_DATA_CONFIG'), data_filename.with_suffix(".json"))

    @classmethod
    @property
    def table_drop_order(cls):
        return [Stringdb_BLAST_KEGG_KEGGID.__table__,
                cls.__table__,
                ]

    @classmethod
    def parse(cls, debug=False):
        """

        :param debug:
        :return:
        """
        nrows = 1000 if debug else None
        df = pd.read_csv(cls.data_path,
                         compression='gzip',
                         sep='\t',
                         nrows=nrows)
        return df

    @classmethod
    def _get_implemented_fields(cls, all_fields, return_deferred_fields=False):

        implemented_fields = ["BLAST_KEGG_KEGGID",
                              "SGD_ID",
                              ]
        if return_deferred_fields:
            return [x for x in all_fields if x not in implemented_fields]
        else:
            return implemented_fields

    @classmethod
    def set_config(cls):
        """

        :return:
        """

        # prepare config
        df = cls.parse()

        # identifies unique fields
        unique_sources = sorted(list(df['source'].unique()))

        # gets max length for each field
        df['length'] = df['alias'].apply(len)
        max_lengths_for_each_source = df.loc[df.groupby('source')['length'].idxmax()]

        # gets fields to implement
        implemented_fields = cls._get_implemented_fields(unique_sources)

        # makes config dict
        config_dict = {'sources': unique_sources,
                       'max_lengths': dict(sorted(zip(max_lengths_for_each_source['source'],
                                                      max_lengths_for_each_source['length']),
                                                  key=lambda x: x[0])),
                       'implemented_fields': implemented_fields
                       }

        # dumps config dict
        with open(cls.config_path, 'w') as f:
            json.dump(config_dict, f, indent=2)
            logger.info(f"Wrote data source names in {cls.data_path} to {cls.config_path}")

    @classmethod
    def load_config(cls):
        def load_():
            with open(cls.config_path, 'r') as f:
                conf_ = json.load(f)
                return conf_
        while True:
            try:
                conf = load_()
                return conf
            except FileNotFoundError:
                logger.warning(f"No config file found in {cls.config_path}. Rerunning config")
                cls.set_config()
                conf = load_()
                return conf

    @classmethod
    def populate(cls, repopulate=False, eng=engine):
        conf = cls.load_config()

        # Table pre-formatting
        if repopulate:
            logger.info(f"repopulating Table {cls.__tablename__} and dependent tables")
            cls.drop_tables(cls.table_drop_order, checkfirst=False, eng=eng)
        Base.metadata.create_all(bind=eng, checkfirst=True)

        # removes rows not to be imported yet. Anticipates not needing to write declarative mappings for all columns
        df = cls.parse()
        df = df.loc[df['source'].isin(conf['implemented_fields'])]
        unique_protein_ids = df['#string_protein_id'].unique()
        alias_object_list = [cls(protein_id=x) for x in unique_protein_ids]
        with Session() as s:
            s.add_all(alias_object_list)
            s.commit()
            logger.info(f"Added {len(alias_object_list)} rows to {cls.__name__}")
        # gets rows by string_protein_id
        for i, id_ in enumerate(unique_protein_ids):
            aliases = df.loc[df['#string_protein_id'] == id_]
            rows = []
            for field in conf['implemented_fields']:
                values = aliases.loc[aliases['source'] == field, 'alias']
                # class_ = getattr(__import__(__name__))
                # to_add = [class_()]
                if field == 'BLAST_KEGG_KEGGID':
                    rows.extend([Stringdb_BLAST_KEGG_KEGGID(kegg_id=x, stringdb_protein_id=id_)
                                 for x in values])
            #         print(rows)
            #     print(field)
            #     print(values)
            # print('\n')
            with Session() as s:
                s.add_all(rows)
                s.commit()
            # if i > 20:
            #     get_size(Stringdb_BLAST_KEGG_KEGGID)
            #     raise NotImplementedError
        get_size(Stringdb_BLAST_KEGG_KEGGID)
        # with Session() as s:
        #     for i, row in chunk.iterrows():
        #         instance = cls(**{'protein_id': row['#string_protein_id'],
        #                           row['source']: row['alias']
        #                           })
        #         db_rows.append(instance)
        #         s.add_all(db_rows)
        #         s.commit()

    # Column mapping
    protein_id = Column(String(16), primary_key=True)
    BLAST_KEGG_EC = Column(String(16))
    BLAST_KEGG_GENEID = Column(Integer)
    # BLAST_KEGG_KEGGID = Column(String(16))
    BLAST_KEGG_KEGGID = relationship('Stringdb_BLAST_KEGG_KEGGID', back_populates='stringdb_protein_alias')
    BLAST_KEGG_NAME = Column(Text)
    BLAST_KEGG_NAME_SYNONYM = Column(String(12))
    BLAST_KEGG_NCBI = Column(String(12))
    BLAST_KEGG_PRODUCT = Column(Text)
    BLAST_UniProt_AC = Column(String(12))
    BLAST_UniProt_DE_AltName_EC = Column(String(12))
    BLAST_UniProt_DE_AltName_Full = Column(Text)
    BLAST_UniProt_DE_AltName_Short = Column(Text)
    BLAST_UniProt_DE_RecName_EC = Column(String(12))
    BLAST_UniProt_DE_RecName_Full = Column(Text)
    BLAST_UniProt_DE_RecName_Short = Column(Text)
    BLAST_UniProt_DR_GeneID = Column(Integer)
    BLAST_UniProt_DR_PDB = Column(String(4))
    BLAST_UniProt_DR_RefSeq = Column(String(16))
    BLAST_UniProt_DR_SGD = Column(String(12))
    BLAST_UniProt_GN_Name = Column(String(12))
    BLAST_UniProt_GN_ORFNames = Column(String(24))
    BLAST_UniProt_GN_OrderedLocusNames = Column(String(12))
    BLAST_UniProt_GN_Synonyms = Column(String(16))
    BLAST_UniProt_ID = Column(String(12))
    Ensembl_EC_NUMBER = Column(String(12))
    Ensembl_EMBL = Column(String(8))
    Ensembl_EntrezGene = Column(String(12))
    Ensembl_EntrezGene_synonym = Column(String(12))
    Ensembl_MEROPS = Column(String(8))
    Ensembl_PDB = Column(String(4))
    Ensembl_RefSeq = Column(String(16))
    Ensembl_RefSeq_short = Column(String(8))
    Ensembl_SGD_GENE = Column(String(10))
    Ensembl_SGD_GENE_synonym = Column(Text)
    Ensembl_SGD_TRANSCRIPT = Column(String(10))
    Ensembl_Source = Column(String(48))
    Ensembl_UniParc = Column(String(16))
    Ensembl_UniProt = Column(String(8))
    Ensembl_UniProt_AC = Column(String(10))
    Ensembl_UniProt_DE_AltName = Column(Text)
    Ensembl_UniProt_DE_RecName = Column(Text)
    Ensembl_UniProt_DR_GeneID = Column(String(8))
    Ensembl_UniProt_DR_PDB = Column(String(4))
    Ensembl_UniProt_DR_RefSeq = Column(String(16))
    Ensembl_UniProt_DR_SGD = Column(String(12))
    Ensembl_UniProt_GN = Column(String(20))
    Ensembl_UniProt_ID = Column(String(12))
    Ensembl_UniProt_synonym = Column(String(6))
    Ensembl_WikiGene = Column(String(10))
    Ensembl_description = Column(Text)
    Ensembl_gene = Column(String(10))
    Ensembl_protein_id = Column(String(10))
    Ensembl_transcript = Column(String(10))
    Ensembl_translation = Column(String(10))
    SGD_ID = Column(String(10))
    SGD_PRIMARY = Column(String(10))
    SGD_SYNONYM = Column(Text)

# Many to one


class Stringdb_BLAST_KEGG_KEGGID(Base):
    __tablename__ = 'stringdb_blast_kegg_keggid'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    kegg_id = Column(String(16))
    stringdb_protein_id = Column(String(16),
                                 ForeignKey('stringdb_protein_aliases.protein_id', ondelete='CASCADE'),
                                 nullable=False)

    stringdb_protein_alias = relationship('StringdbAlias', back_populates='BLAST_KEGG_KEGGID')

