from sqlalchemy import Column, Integer, String, Numeric
from app.database.base import Base


class Apartment(Base):
    __tablename__ = 'apartments'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    city = Column(String(200), nullable=False)
    bedrooms = Column(Integer, nullable=False)
    max_guests = Column(Integer, nullable=False)
    nightly_rate = Column(Numeric(10,2), nullable=False)
    status = Column(String(50), nullable=False, default="available") 
