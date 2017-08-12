from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

from . import settings


DeclarativeBase = declarative_base()

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))

class ScrapedSephoraProduct(DeclarativeBase):
    """"""
    __tablename__ = "scraped_sephora_products"

    id = Column(Integer, primary_key=True)
    name = Column('name', String)
    brand = Column('brand', String)
    sephora_id = Column('sephora_id', String)
    image_url = Column('image_url', String)
    url = Column('url', String)
    source = Column('source', Text)
    category = Column('url', String)
    scraped_at = Column('scraped_at', DateTime)
    inserted_at = Column('inserted_at', DateTime)
    updated_at = Column('updated_at', DateTime)

class ScrapedSephoraReview(DeclarativeBase):
    """"""
    __tablename__ = "scraped_sephora_reviews"

    id = Column(Integer, primary_key=True)
    sephora_id = Column('sephora_id', String)
    text = Column('text', Text)
    url = Column('url', String)
    review_json = Column('review_json', JSONB)
    scraped_at = Column('scraped_at', DateTime)
    inserted_at = Column('inserted_at', DateTime)
    updated_at = Column('updated_at', DateTime)
