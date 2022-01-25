
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


class ProteinLinks(Base):

    __tablename__ = "protein_links"
    __table_args__ = {"extend_existing": True}
    data_relative_path = Path("external_data/string-db/by-organism/Saccharomyces-cerevisiae/"
                              "4932.protein.links.full.v11.5.txt")
    column_names = [
        ""
    ]

    @classmethod
    def parse(cls):
        for chunk in pd.read_csv(cls.data_relative_path,
                                 sep=" ",
                                 chunksize=100000,
                                 nrows=1000):
            print(chunk)
            raise NotImplementedError



    id = Column(Integer, primary_key=True)
    protein = Column(String(16), index=True, nullable=False)
    interacter = Column(String(16), index=True, nullable=False)
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
