from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # Relationship to Product model
    products = relationship("Product", back_populates="category")
