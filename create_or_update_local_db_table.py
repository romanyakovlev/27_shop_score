from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from main import db


local_engine = create_engine('postgres://roman:ilovecska9@localhost/testdb')

if __name__ == "__main__":
    base_class = declarative_base()
    base_class.metadata.reflect(db.engine)
    base_class.metadata.create_all(local_engine)
