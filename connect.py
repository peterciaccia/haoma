"""
Created 2021-10-12
Connects to mysql container when imported
"""

import os
from sqlalchemy import create_engine

from library import uniprot
from dotenv import load_dotenv

load_dotenv()

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

# connect to database
print(connection_str)
engine = create_engine(connection_str)


# idmapping

# connection = engine.connect()
# # pull metadata of a table
# metadata = db.MetaData(bind=engine)
# metadata.reflect(only=['test_table'])

# Session = sessionmaker(bind=engine)
# session = Session()




