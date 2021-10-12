"""

"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


# engine = create_engine("sqlite:///some.db", future=True)

# mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
engine = create_engine("mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>")

connection = engine.connect()

Base = declarative_base()

class Annotation(Base):

    __tablename__ = 'Uniprot_IDMapping'

