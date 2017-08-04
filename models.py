from sqlalchemy.ext.declarative import declarative_base
from main import db


base_class = declarative_base()
base_class.metadata.reflect(db.engine)


class Shop(base_class):
    __table__ = base_class.metadata.tables['orders']
