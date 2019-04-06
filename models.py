from sqlalchemy import Integer, Column, String, DateTime
from workspace.database import Base
from sqlalchemy.sql import func

class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String(50), unique=True)
    date_created = Column(DateTime(), server_default=func.now())
    country = Column(String(3), default='TnT')

    def __init__(self, name, country = None):
        self.name = name
        if country:
            self.country = country
        

    def toDict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date_created': self.date_created,
            'country': self.country
        }