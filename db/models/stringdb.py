
# built-ins
import os
from pathlib import Path

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

    # @declared_attr
    # def delete_if_repopulate(cls):
    #     return [
    #     # another DeclarativeTable.__table__,
    #     StringdbProteinLink.__table__
    # ]

    @classmethod
    def parse(cls, debug=False):

        nrows = 1000 if debug else None
        for chunk in pd.read_csv(cls.data_path,
                                 compression='gzip',
                                 sep=' ',
                                 chunksize=100000,
                                 nrows=nrows):
            chunk.rename(columns={'protein1': 'protein', 'protein2': 'interacter'}, inplace=True)
            yield chunk

    @classmethod
    def populate(cls, eng=engine, repopulate=False, debug=False):
        # TODO: make delete_if_repopulate an abstractproperty in the Base. Then define list of tables to drop outside
        # TODO: of this method
        delete_if_repopulate = [cls.__table__,
                                # another DeclarativeTable.__table__
                                ]
        # Table pre-formatting
        if repopulate:
            cls.drop_tables(delete_if_repopulate, eng=eng)
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

    protein = Column(String(16), primary_key=True, nullable=False)
    interacter = Column(String(16), primary_key=True, nullable=False)
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

    @classmethod
    def parse(cls, debug=False):

        nrows = 1000 if debug else None
        for chunk in pd.read_csv(cls.data_path,
                                 compression='gzip',
                                 sep='\t',
                                 chunksize=100000,
                                 nrows=nrows):
            yield chunk

    @classmethod
    def populate(cls, repopulate=False, eng=engine):
        # Table pre-formatting
        if repopulate:
            cls.repopulate(eng=eng)
        Base.metadata.create_all(bind=eng, checkfirst=True)

