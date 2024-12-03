from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.database import Base

class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    cost = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=True)
    unit_id = Column(Integer, ForeignKey('unit.id'), nullable=True)
    brand_id = Column(Integer, ForeignKey('brand.id'), nullable=True)
    tag_id = Column(Integer, ForeignKey('tag.id'), nullable=True)
    description = Column(Text, nullable=True)
    image = Column(String, default="/static/uploaded_images/default.png")

    # Relationships
    category = relationship('Category', back_populates='products')
    unit = relationship('Unit', back_populates='products')
    brand = relationship('Brand', back_populates='products')
    tag = relationship('Tag', back_populates='products')
