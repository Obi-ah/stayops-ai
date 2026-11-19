from app.database.connection import engine
from app.database.base import Base

from app.models.apartment import Apartment

def create_tables():
    Base.metadata.create_all(bind=engine)