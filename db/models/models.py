
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    firstname = Column(String(30))
    lastname = Column(String(30))
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
