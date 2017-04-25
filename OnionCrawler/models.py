from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import settings


DeclarativeBase = declarative_base()


def db_connect():

    return create_engine(URL(**settings.DATABASE))


def create_memex_table(engine):
    
    DeclarativeBase.metadata.create_all(engine)


class CrawlerData(DeclarativeBase):
    __tablename__ = "memex"

    id = Column(Integer, primary_key=True)
    time = Column('time', DateTime, nullable=True)
    url = Column('url', String, nullable=True)
    #title = Column('title', String, nullable=True)
    body = Column('body', String, nullable=True)