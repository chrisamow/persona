#!/usr/bin/env python3

from sys import argv
from sqlalchemy import (Column, Integer, Date, String)
from sqlalchemy.ext.declarative import declarative_base                         
from sqlalchemy import Sequence
#import datetime

Base = declarative_base()   #standard sqlalchemy stuff




class Person(Base):
    """the only model for this project"""
    __tablename__ = 'person'
    namemax = 255
    id = Column(Integer, Sequence('person_id_seq'), primary_key=True)
    lastname = Column(String(namemax))
    firstname = Column(String(namemax))
    dateofbirth = Column(Date)
    zipcode = Column(Integer)
    pass


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from settings import DB_URI
    if 'createdb' in argv:
        engine = create_engine(DB_URI)
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

