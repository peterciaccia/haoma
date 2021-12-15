import os

import pandas as pd
from sqlalchemy import Column, String, Integer, ForeignKey, text
from sqlalchemy.orm import relationship
from db import Base, Session
from db.models.refseq import logger
from db.utils import get_size


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    firstname = Column(String(30), nullable=False)
    lastname = Column(String(30), nullable=False)
    username = Column(String(60), nullable=False, server_default=text('1'))
    nickname = Column(String(60))

    email_addresses = relationship('Email', back_populates='user')

    def __repr__(self):
        return f"<User(name={self.firstname} {self.lastname})>"


class Email(Base):
    __tablename__ = 'email_addresses'

    id = Column(Integer, primary_key=True)
    email_address = Column(String(128), nullable=False)
    used_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='email_addresses')


class RefSeq_to_Uniprot(Base):
    __tablename__ = 'refseq_to_uniprot'

    RefSeq_id = Column('RefSeq_id', String(16), primary_key=True)
    UniProtKB_AC = Column('UniProtKB_AC', String(16), primary_key=True)

    def __repr__(self):
        return f"RefSeq(RefSeq_id={self.RefSeq_id!r}, UniProtKB_AC={self.UniProtKB_AC!r}"

    @classmethod
    def parse(cls, debug=False, chunksize=None, nrows=None):
        """
        :param debug:
        :param chunksize:
        :param nrows:
        :return:
        """
        default_chunksize = 100000
        path_from_data_root = "ncbi/refseq/uniprotkb/gene_refseq_uniprotkb_collab"
        if chunksize is None:
            chunksize = default_chunksize
        if debug:
            if nrows is None:
                nrows=250000
            logger.debug(f'chunk size set to {chunksize}')

        data_path = os.path.join(os.getenv('EXTERNAL_DATA_DIR'), path_from_data_root)
        for chunk in pd.read_csv(
                data_path,
                delimiter='\t',
                names=["RefSeq", "UniProtKB_AC"],
                skiprows=1,
                chunksize=chunksize,
                nrows=nrows
        ):
            yield chunk

        # logger.debug(f'refseq table read into {len(chunks)} chunks')

    @classmethod
    def populate(cls, chunklist, eng, debug=False, repopulate=False):
        """
        :param chunklist: list of pandas dfs
        :param eng:
        :param debug:
        :param repopulate:
        :return:
        """

        if repopulate:
            to_deletes = [RefSeq_to_Uniprot.__table__]
            Base.metadata.drop_all(bind=eng, tables=to_deletes)
        Base.metadata.create_all(bind=eng, checkfirst=True)
        # get_size(RefSeq_to_Uniprot, verbose=True)
        for df in chunklist:
            rows = [RefSeq_to_Uniprot(RefSeq_id=x, UniProtKB_AC=y) for x, y in zip(df['RefSeq'], df['UniProtKB_AC'])]
            with Session() as s:
                s.add_all(rows)
                s.commit()
        get_size(RefSeq_to_Uniprot, verbose=True)
