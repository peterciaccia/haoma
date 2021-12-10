"""
Created by Peter Ciaccia on 2021-12-09
Purpose: test querying
Findings:
Follow-up:
"""

# dependencies
import os
from dotenv import load_dotenv
import pandas as pd

# internal
import logging
import test_tools
from db import engine, Base, Session
from db.models.models import User, Email

load_dotenv()
logging.basicConfig(filename=test_tools.get_log_path(),
                    filemode="w",
                    level=logging.DEBUG,
                    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    # force=True
                    )

names_and_emails_path = os.path.join(os.getenv('PROJECT_DIR'), 'resources/test_data/names_and_emails.txt')
column_names = ['name', 'surname', 'email_address']

names_and_emails_df = pd.read_csv(names_and_emails_path, names=column_names, sep='\t')
print(names_and_emails_df)

Base.metadata.create_all(bind=engine, checkfirst=True)

with Session() as s:
    rows = [User(firstname=name, lastname=surname, email_addresses=[Email(email_address=email)])
            for name, surname, email in zip(names_and_emails_df['name'],
                                            names_and_emails_df['surname'],
                                            names_and_emails_df['email_address']
                                            )
            ]
    s.add_all(rows)
    s.commit()
