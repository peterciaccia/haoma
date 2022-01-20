
# built-ins
import os

# dependencies
import pandas as pd
from sqlalchemy import Column, String, Integer, ForeignKey, text
from sqlalchemy.orm import relationship

# in-app
from db import Session
from db.Base import Base
from db.utils import get_size
import log.conf
logger = log.conf.get_logger(module='test')


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
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='email_addresses')


class RefSeq_to_Uniprot(Base):
    __tablename__ = 'refseq_to_uniprot'

    RefSeq_id = Column('RefSeq_id', String(16), primary_key=True)
    UniProtKB_AC = Column('UniProtKB_AC', String(16), primary_key=True)

    def __repr__(self):
        return f"RefSeq(RefSeq_id={self.RefSeq_id!r}, UniProtKB_AC={self.UniProtKB_AC!r}"

    @classmethod
    def parse(cls, debug=False, chunk_size=None, nrows=None):
        """
        :param debug:
        :param chunk_size:
        :param nrows:
        :return:
        """
        default_chunk_size = 100000
        path_from_data_root = "ncbi/refseq/uniprotkb/gene_refseq_uniprotkb_collab"
        if chunk_size is None:
            chunk_size = default_chunk_size
        if debug:
            if nrows is None:
                nrows=250000
            logger.debug(f'chunk size set to {chunk_size}')

        data_path = os.path.join(os.getenv('EXTERNAL_DATA_DIR'), path_from_data_root)
        for chunk in pd.read_csv(
                data_path,
                delimiter='\t',
                names=["RefSeq", "UniProtKB_AC"],
                skiprows=1,
                chunksize=chunk_size,
                nrows=nrows
        ):
            # generator handles read_csv
            try:
                yield chunk
            except (TypeError, StopIteration):
                # TODO check that this is the most correct way to handle the end of a generator
                logger.warning('check generator ending')
                return

    @classmethod
    def populate(cls, chunks, eng, debug=False, repopulate=False):
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
        for df in chunks:
            rows = [RefSeq_to_Uniprot(RefSeq_id=x, UniProtKB_AC=y) for x, y in zip(df['RefSeq'], df['UniProtKB_AC'])]
            with Session() as s:
                s.add_all(rows)
                s.commit()

        # TODO: get # lines with a session call
        _temp = '"Unimplemented"'
        logger.debug(f'{_temp} lines added')

        get_size(RefSeq_to_Uniprot, debug=True)
