import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, ARRAY, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import psycopg2


Base = declarative_base()


class Jobs(Base):
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True)
    image_url = Column(String(200), nullable=False)
    labels_things = Column(ARRAY(String))
    labels_stuff = Column(ARRAY(String))
    mask_labels = Column(ARRAY(String))
    masks_nparr = Column(LargeBinary)  # BYTEA datatype in database; use pickle to load and dump from np array to binary
    result_image_url = Column(String(200))
    status = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

    def __repr__(self):
        return '<Jobs: {0}:\n -> status:{1}; updated_at:{2}>'.format(self.image_url,
                                                                    self.status,
                                                                    self.updated_at)


engine = create_engine('postgres+psycopg2://postgres:root@localhost:5432/pyvinci')

Base.metadata.create_all(engine)