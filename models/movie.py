from config.database import Base
from sqlalchemy import Column, Integer, String, Float

class Movie(Base):
    
    __table__='movies'#name of the database
    #Columns on the sql database
    id=Column(Integer, primary_key=True)
    title=Column(String)
    Review=Column(String)
    Year=Column(Integer)
    Rating=Column(Float)
    Category=Column(String)
    
    
    
    
