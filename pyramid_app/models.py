from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
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
    search = Column(Text)

    def __init__(self, username, search):
        self.username = username
        self.search = search

class SearchTable(Base):
    __tablename__ = 'search'
    search_id = Column(Integer, ForeignKey('users.id'), primary_key = True)
    search_content = Column(Text)

    def __init__(self, search_content):
        self.search_content = search_content