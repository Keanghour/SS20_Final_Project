# db\user.py

from sqlalchemy import Column, Integer, String
from db.database import Base

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    address = Column(String, nullable=False)
    image = Column(String, default='default.png')
    

