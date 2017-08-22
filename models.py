from sqlalchemy.ext.declarative import declarative_base
from main import db
from create_or_update_local_db_table import local_engine


base_class = declarative_base()
base_class.metadata.reflect(local_engine)


class Shop(base_class):
    __table__ = base_class.metadata.tables['orders']
