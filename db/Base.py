
import os
from pathlib import Path

# dependencies
from sqlalchemy.ext.declarative import declared_attr, declarative_base

# in-app
from db import engine


class AbstractBase(object):

    data_relative_path = Path()

    @declared_attr
    def data_path(cls):
        return os.path.join(os.getenv('EXTERNAL_DATA_BASENAME'), cls.data_relative_path)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Base = declarative_base(cls=AbstractBase)
Base.metadata.create_all(engine)
