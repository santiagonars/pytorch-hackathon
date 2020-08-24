import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, ARRAY, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import psycopg2

# os.environ['WORKER_DATABASE_URL'] = 'postgres+psycopg2://postgres:root@localhost:5432/pyvinci'
DATABASE_URL = os.getenv('WORKER_DATABASE_URL')
Base = declarative_base()


class UserRecord(Base):
    __tablename__ = 'user_record'
    
    id = Column(Integer, primary_key=True)
    # username = Column(String, nullable=False)
    # password = Column(String, nullable=False)
    # created_at = Column(TIMESTAMP, nullable=False)
    # updated_at = Column(TIMESTAMP, nullable=False)


class Project(Base):
    __tablename__ = 'project'
    
    id = Column(Integer, primary_key=True)
    user_record = Column(Integer, ForeignKey('user_record.id'), nullable=False)
    keywords = Column(ARRAY(String))
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

    def __repr__(self):
        return '<project id={0}\n -> user_record={1}\n -> created_at={2}; updated_at={3}>'.format(self.id,
                                                                                                self.user_record,
                                                                                                self.created_at,
                                                                                                self.updated_at)
                                                                                

class Image(Base):
    __tablename__ = 'image'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)
    url = Column(String(200), nullable=False)
    labels_things = Column(ARRAY(String))
    labels_stuff = Column(ARRAY(String))
    masks_labels = Column(ARRAY(String))
    masks = Column(LargeBinary)  # BYTEA datatype in database; use pickle to load and dump from np array to binary
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

    def __repr__(self):
        return '<image id={0}\n -> project_id={1}\n -> url={2}\n -> created_at={3}; updated_at={4}>'.format(self.id,
                                                                                                    self.project_id,
                                                                                                    self.url,
                                                                                                    self.created_at,
                                                                                                    self.updated_at)                                                                                    


class Jobs(Base):
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)
    result_image_url = Column(String(200))
    status = Column(String(15), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

    def __repr__(self):
        return '<job id={0}\n -> project_id={1}\n -> status={2}\n -> created_at={3}; updated_at={4}>'.format(self.id,
                                                                                                    self.project_id,
                                                                                                    self.status,
                                                                                                    self.created_at,
                                                                                                    self.updated_at)


# engine = create_engine('postgres+psycopg2://postgres:root@localhost:5432/pyvinci')
engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)

