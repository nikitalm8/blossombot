import config

from sqlalchemy import Column, BigInteger, Integer, String

from . import Base


class Guild(Base):
    __tablename__ = 'guilds'

    Id = Column('id', BigInteger, primary_key=True)
    Prefix = Column('prefix', String(10), default=config.DEFAULT_PREFIX)
    Language = Column('language', Integer, default=0)
