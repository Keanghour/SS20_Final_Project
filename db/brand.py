from sqlalchemy import Column, Integer, String
from db.database import Base
from sqlalchemy.orm import relationship

class Brand(Base):
    __tablename__ = 'brand'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    # Relationship to Product model
    products = relationship('Product', back_populates='brand')
