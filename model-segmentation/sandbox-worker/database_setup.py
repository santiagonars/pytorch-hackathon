import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, ARRAY, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import psycopg2
# from psycopg2 import sql

Base = declarative_base()

# ---------WIll NEED this below to load NP_ARRAY (masks) using PICKLE:----------
# https://stackoverflow.com/questions/60278766/best-way-to-insert-python-numpy-array-into-postgresql-database
# https://docs.sqlalchemy.org/en/13/core/type_basics.html#sqlalchemy.types.PickleType

class Jobs(Base):
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True)
    imageurl = Column(String(100), nullable=False)

    labels_things = Column(ARRAY(String))
    labels_stuff = Column(ARRAY(String))
    mask_labels = Column(ARRAY(String))
    masks_nparr = Column(LargeBinary)  # BYTEA datatype in database

    status = Column(String(8), nullable=False)

    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)



engine = create_engine('postgres+psycopg2://postgres:root@localhost:5432/pyvinci')

# Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)

