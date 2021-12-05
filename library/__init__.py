"""
Created by Peter Ciaccia
"""
import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeferredReflection
from sqlalchemy.orm import sessionmaker

load_dotenv()

# configures db connection
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

# specifies connection string
connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'
logging.debug(f'MySQL Connection string:\t{connection_str}')

# creates engine
engine = create_engine(connection_str)
DeferredReflection.prepare(engine)

# Constructs Session class declaration
Session = sessionmaker(bind=engine)
