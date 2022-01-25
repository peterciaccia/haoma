
import os
from pathlib import Path

# dependencies
from sqlalchemy.ext.declarative import declared_attr, declarative_base

# in-app
from db import engine
from db.utils import get_size

import log.conf
logger = log.conf.get_logger(module='test')


class AbstractBase(object):

    data_relative_path = Path()

    @declared_attr
    def data_path(cls):
        return os.path.join(os.getenv('EXTERNAL_DATA_BASENAME'), cls.data_relative_path)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod
    def drop_tables(cls, to_deletes, eng=engine):
        get_size(cls)
        double_check = input(f"Are you sure you want to drop table {cls.__tablename__} and its "
                             f"{get_size(cls, log=False)} rows?\nType 'y' to proceed\n")
        if double_check == 'y':
            Base.metadata.drop_all(bind=eng, tables=to_deletes)
            logger.warning(f"Table {cls.__tablename__} dropped")


Base = declarative_base(cls=AbstractBase)
Base.metadata.create_all(engine)
