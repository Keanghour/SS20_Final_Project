from sqlalchemy import Column, Integer, String
from db.database import Base
from sqlalchemy.orm import relationship

class Unit(Base):
    __tablename__ = 'unit'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    # Relationship to Product model
    products = relationship('Product', back_populates='unit')
