from sqlalchemy.ext.declarative import declarative_base
from main import db


Base = declarative_base()
Base.metadata.reflect(db.engine)


class Shop(Base):
    __table__ = Base.metadata.tables['orders']
