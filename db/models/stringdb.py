
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
            chunk.rename(columns={'protein1': 'protein_id', 'protein2': 'interacter_id'}, inplace=True)
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
    def parse(cls, debug=False):

        nrows = 1000 if debug else None
        for chunk in pd.read_csv(cls.data_path,
                                 compression='gzip',
                                 sep='\t',
                                 chunksize=100000,
                                 nrows=nrows):
            yield chunk

    @classmethod
    def generate_unique_source_names(cls):

        unique_sources = []
        chunklist = []
        for chunk in pd.read_csv(cls.data_path,
                                 compression='gzip',
                                 sep='\t',
                                 chunksize=100000):
            unique_sources.extend(chunk['source'].unique())
            chunk['length'] = chunk['alias'].apply(len)
            chunklist.append(chunk)
        df = pd.concat(chunklist)
        max_values = df.loc[df.groupby('source')['length'].idxmax()]
        config_dict = {'unique_sources': dict(sorted(zip(max_values['source'],
                                                         max_values['length']),
                                                     key=lambda x: x[0]))
                       }
        with open(cls.config_path, 'w') as f:
            json.dump(config_dict, f, indent=2)
            logger.info({f"Wrote data source names in {cls.data_path} to {cls.config_path}"})


    @classmethod
    def load_config(cls):
        with open(cls.config_path, 'r') as f:
            conf = json.load(f)
        df = pd.DataFrame(columns=['string_protein_id'].extend(conf['unique_sources']))
        return df

    @classmethod
    def populate(cls, repopulate=False, eng=engine):
        # Table pre-formatting
        if repopulate:
            cls.drop_tables(eng=eng)
        Base.metadata.create_all(bind=eng, checkfirst=True)

