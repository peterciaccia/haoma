"""
Created 2021-10-12
Connects to mysql container when imported
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from library import uniprot
from dotenv import load_dotenv
load_dotenv()

config = {
    'host': 'localhost',
    'port': 3306,
    'user': os.getenv('MYSQL_NAME'),
    'password': os.getenv('MYSQL_PASS'),
    'database': 'haomalib'
}

db_user = config.get('user')
db_pwd = config.get('password')
db_host = config.get('host')
db_port = config.get('port')
db_name = config.get('database')

# db_user = 'root'
# db_pwd = 'ezekiel23_20!dsfdf'

# specify connection string
connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'
# connection_str= f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/sqlalchemy'
# connect to database
print(connection_str)
engine = create_engine(connection_str)
uniprot.Base.metadata.create_all(bind=engine)
# connection = engine.connect()
# # pull metadata of a table
# metadata = db.MetaData(bind=engine)
# metadata.reflect(only=['test_table'])

# Session = sessionmaker(bind=engine)
# session = Session()



# test_table = metadata.tables['test_table']
