from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
    orm
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class UsersTable(Base):
    __tablename__ = 'users'
    id  = Column(Integer, primary_key = True, nullable = False, autoincrement = True)
    username = Column(Text, unique = True, nullable = False)
    password = Column(Text, nullable = False)
    group = Column(Text, nullable = False)

    def __init__(self, username, password, group):
        self.username = username
        self.password = password
        self.group = group

    def to_str(self):
        return str(self.id), self.username, self.password, self.group

class SearchTable(Base):
    __tablename__ = 'search'
    search_id = Column(Integer, primary_key = True)
    search_content = Column(Text, primary_key = True, nullable = False)
    search_quantity = Column(Integer, nullable = False)

    def __init__(self, user_id, search_content, search_quantity):
        self.search_content = search_content
        self.search_id = user_id
        self.search_quantity = search_quantity

    def to_str(self):
        return str(self.search_id), self.search_content, str(self.search_quantity)