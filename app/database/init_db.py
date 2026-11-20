from app.database.connection import engine
from app.database.base import Base

from app.models.apartment import Apartment
from app.models.guest import Guest
from app.models.booking import Booking

def create_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
