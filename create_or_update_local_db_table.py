from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from main import db
import os


local_engine = create_engine(os.environ['DB_URI'])

if __name__ == "__main__":
    base_class = declarative_base()
    base_class.metadata.reflect(db.engine)
    base_class.metadata.create_all(local_engine)
