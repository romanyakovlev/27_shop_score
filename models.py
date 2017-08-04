from sqlalchemy.ext.declarative import declarative_base
from main import db


Base_class = declarative_base()
Base_class.metadata.reflect(db.engine)


class Shop(Base_class):
    __table__ = Base_class.metadata.tables['orders']
