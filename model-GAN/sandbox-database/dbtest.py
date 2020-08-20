from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.database_setup import Base, Jobs


engine = create_engine('postgres+psycopg2://postgres:root@localhost:5432/pyvinci')
# Bind the engine to the metadata of the Base class
Base.metadata.bind = engine

# A DBSession() instance establishes all communications with the database
DBSession = sessionmaker(bind=engine)

# session.commit() => use to make any changes in the database
# session.rollback() => use to revert all changes back to the the last commit
session = DBSession()