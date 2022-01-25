"""
Created by Peter Ciaccia
This module contains Declarative mappings for SGD feature annotations and the methods to populate these tables.
"""
# built-ins
import os
from pathlib import Path

# dependencies
import pandas as pd
from sqlalchemy import Column, String, Integer, Float, Date, Text, ForeignKey
from sqlalchemy.orm import relationship

# in-app
from db import engine
from db.Base import Base
from db import Session
from db.utils import get_size
import log.conf
logger = log.conf.get_logger(module='test')


class SgdFeature(Base):

    __tablename__ = 'sgd_features'
    __table_args__ = {'extend_existing': True}
    data_relative_path = Path('external_data/SGD/curation/chromosomal_feature/SGD_features.tab')
    _use_cols = list(range(14)) + [15]
    column_names = [
        'sgd_id',
        'feature_type',
        'feature_qualifier',
        'feature_name',
        'standard_name',
        'aliases',
        'parent_feature_name',
        'secondary_sgd_id',
        'chromosome',
        'start_coordinate',
        'stop_coordinate',
        'strand',
        'genetic_position',
        'coordinate_version',
        'description'
    ]

    id = Column(Integer, primary_key=True)
    sgd_id = Column(String(16), index=True, nullable=False)
    feature_type = Column(String(36), nullable=False)
    feature_qualifier = Column(String(24))
    feature_name = Column(String(16))
    standard_name = Column(String(16))
    aliases = relationship('SgdAlias', back_populates='sgd_feature')
    parent_feature_name = Column(String(16))
    secondary_sgd_id = relationship('SecondarySgdId', back_populates='sgd_feature')
    chromosome = Column(String(8))
    start_coordinate = Column(Integer)
    stop_coordinate = Column(Integer)
    strand = Column(String(1))
    genetic_position = Column(Float)
    coordinate_version = Column(Date)
    # sequence_version not imported
    description = Column(Text)

    def __repr__(self):
        return f"<SgdFeatures(name={self.feature_name} sgd_id={self.sgd_id})>"

    @classmethod
    def _get_simple_column_names(cls):
        _simple_column_tup = (0, 1, 2, 3, 4, 6, 8, 9, 10, 11, 12, 13, 14)
        return [cls.column_names[i] for i in _simple_column_tup]

    @classmethod
    def _get_compound_column_names(cls):
        _compound_column_tup = (5, 7)
        return [cls.column_names[i] for i in _compound_column_tup]

    @classmethod
    def _instantiate_list(cls, name_list, DeclarativeTable, *args, **kwargs):\
        return [DeclarativeTable(**{}) for name in name_list]

    @classmethod
    def parse(cls, nrows=None):

        # reads SGD features
        df = pd.read_csv(
            cls.data_path,
            delimiter='\t',
            names=cls.column_names,
            usecols=cls._use_cols,
            nrows=nrows
        )
        # Splits "|"-delimited fields into lists
        _compound_column_names = cls._get_compound_column_names()
        for col in _compound_column_names:
            df[col] = df[col].str.split('|')
        # replaces NaN with None for sqlalchemy import
        df = df.where(pd.notnull(df), None)
        # Converts values in compound columns from None to empty list
        for col in _compound_column_names:
            df[col] = df[col].apply(lambda x: [] if x is None else x)

        return df

    @classmethod
    def populate(cls, eng=engine, debug=False, repopulate=False):
        """
        :param chunklist: list of pandas dfs
        :param eng:
        :param debug:
        :param repopulate:
        :return:
        """

        if repopulate:
            to_deletes = [
                SgdAlias.__table__,
                SecondarySgdId.__table__,
                SgdFeature.__table__
            ]
            logger.debug(f"repopulating '{cls.__tablename__}'")
            Base.metadata.drop_all(bind=eng, tables=to_deletes)
        Base.metadata.create_all(bind=eng, checkfirst=True)

        df = SgdFeature.parse()
        get_size(cls, debug=debug)

        with Session() as s:
            sgd_feature_list = []

            # imports simple features
            for i, df_row in df.iterrows():
                sgd_feature_list.append(cls(**{x: df_row[x]
                                               for x in cls._get_simple_column_names()
                                               }))
            s.add_all(sgd_feature_list)
            s.commit()
            many_to_one_sgd_objects_list = []

            # imports compound features
            for i, df_row in df.iterrows():
                foreign_key = 'sgd_id'
                many_to_one_sgd_objects_list.extend(
                    [SgdAlias(alias=x, sgd_feature_id=df_row[foreign_key])
                     for x in df_row['aliases']])
                many_to_one_sgd_objects_list.extend(
                    [SecondarySgdId(secondary_sgd_id=x, sgd_feature_id=df_row[foreign_key])
                     for x in df_row['secondary_sgd_id']]
                )
            s.add_all(many_to_one_sgd_objects_list)
            s.commit()

        # TODO: get # lines with a session call
        # _temp = '"Unimplemented"'
        # get_size(cls, debug=debug)
        # logger.debug(f"{_temp} lines added")


"""
Many-to-one relationship tables
"""


class SgdAlias(Base):

    __tablename__ = 'sgd_feature_aliases'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    alias = Column(Text)
    sgd_feature_id = Column(String(16), ForeignKey('sgd_features.sgd_id', ondelete='CASCADE'), nullable=False)

    sgd_feature = relationship('SgdFeature', back_populates='aliases')


class SecondarySgdId(Base):

    __tablename__ = 'secondary_sgd_id'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    secondary_sgd_id = Column(String(48))
    sgd_feature_id = Column(String(16), ForeignKey('sgd_features.sgd_id', ondelete='CASCADE'), nullable=False)

    sgd_feature = relationship('SgdFeature', back_populates='secondary_sgd_id')
