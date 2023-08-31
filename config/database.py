import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqllite_filename='../database.sqlite'

base_dir= os.path.dirname(os.path.realpath(__file__))#this reads the actual directory of the current file

database_url=f'sqlite:///{os.path.join(base_dir,sqllite_filename)}'

engine=create_engine(database_url, echo=True)#The echo parameter shows through the console what is going on

#create session
session=sessionmaker(bind=engine)

Base=declarative_base()