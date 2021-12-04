"""
Created 2021-10-12
Connects to mysql container when imported
"""
import logging
import os
from sqlalchemy import create_engine, MetaData
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.ext.automap import automap_base
load_dotenv()


def stats(eng):
    # metadata_obj = MetaData()
    # metadata_obj.reflect(bind=eng)
    # print([table.name for table in metadata_obj.sorted_tables])
    Base = declarative_base(bind=eng)
    pass
    # meta = uniprot.Base.metadata
    print(Base.metadata)


logging.debug('Creating declarative base instance')
Base = declarative_base()

config = {
    'host': 'localhost',
    'port': 3306,
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASS'),
    'database': os.getenv('DATABASE')
}

db_user = config.get('user')
db_pwd = config.get('password')
db_host = config.get('host')
db_port = config.get('port')
db_name = config.get('database')


# specify connection string
connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'
logging.debug(f'MySQL Connection string:\t{connection_str}')

# creates engine
engine = create_engine(connection_str)
DeferredReflection.prepare(engine)

if __name__ == '__main__':
    logging.debug(f'{__file__} called by self')
    connection = engine.connect()
    stats(engine)





