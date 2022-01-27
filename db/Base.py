
import os
from pathlib import Path

# dependencies
from sqlalchemy.ext.declarative import declared_attr, declarative_base

# in-app
from db import engine

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
    @property
    def table_drop_order(cls):
        return []

    @classmethod
    def drop_tables(cls, to_deletes=None, eng=engine, checkfirst=True):
        def drop():
            # TODO:
            table_names = [x.fullname for x in to_deletes]
            Base.metadata.drop_all(bind=eng, tables=to_deletes)
            logger.warning(f"Tables {table_names} dropped")

        if to_deletes is None:
            to_deletes = cls.table_drop_order
        if not checkfirst:
            drop()
        else:
            response = input(f"Type 'y' to confirm table drop")
            if response == 'y':
                drop()
            else:
                logger.warning(f"No confirmation provided. Tables {to_deletes} not dropped")

    @classmethod
    def defer_implementation(cls):
        pass


Base = declarative_base(cls=AbstractBase)
Base.metadata.create_all(engine)
