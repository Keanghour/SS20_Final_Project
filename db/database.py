
# db\database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database URL
DATABASE_URL = "sqlite:///db/app_db.sqlite"

# Create engine and session maker
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
DBSession = Session

# Base class needed to create tables
Base = declarative_base()

# Initialize the database if it does not exist
def init_db():
    from db.user import User
    from db.product import Product
    from db.category import Category
    from db.unit import Unit
    from db.brand import Brand
    from db.tag import Tag
    Base.metadata.create_all(engine)
