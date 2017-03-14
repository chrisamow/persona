#!/usr/bin/env python3

from sys import argv
from sqlalchemy import (Column, Integer, DateTime, String)
from sqlalchemy.ext.declarative import declarative_base                         
from sqlalchemy import Sequence
import datetime

Base = declarative_base()   #standard sqlalchemy stuff




class Person(Base):
    """the only model for this project"""
    __tablename__ = 'person'
    namemax = 255
    id = Column(Integer, Sequence('person_id_seq'), primary_key=True)
    lastname = Column(String(namemax))
    firstname = Column(String(namemax))
    dateofbirth = Column(DateTime)
    zipcode = Column(Integer)
    def setDob(self, s):
        """ease formatting pain if you have a simple YYYY-MM-DD date"""
        self.dateofbirth = datetime.datetime.strptime(s, '%Y-%m-%d')



if __name__ == "__main__":
    from sqlalchemy import create_engine
    from settings import DB_URI
    if len(argv) > 1:
        command = argv[1]
        engine = create_engine(DB_URI)
        if command == 'createdb':
            Base.metadata.drop_all(engine)
            Base.metadata.create_all(engine)
        elif command == 'sampledata':
            import csv
            from sqlalchemy.orm import sessionmaker
            Session = sessionmaker(bind=engine)
            s = Session()
            #p1 = Person(id=1000, lastname='test', firstname='justa', zipcode='90210')
            #s.add(p1)
            #s.commit()
            with open(argv[2]) as csvfile:
                rdr = csv.reader(csvfile, delimiter=',')
                for row in rdr:
                    per = Person(id=row[0], lastname=row[1], firstname=row[2], zipcode=row[4])
                    per.setDob(row[3])
                    s.add(per)
                    pass
            s.commit()

