
from sqlalchemy import Column, String, Integer
from db.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    nickname = Column(String)

    def __repr__(self):
        return f"<User(name={self.firstname} {self.lastname})>"
