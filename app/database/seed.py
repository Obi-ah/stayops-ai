from app.database.connection import SessionLocal
from app.models.apartment import Apartment

apartments = [
    {
        "name": "Northern Quarter Studio",
        "city": "Manchester",
        "bedrooms": 1,
        "max_guests": 2,
        "nightly_rate": 95.00,
        "status": "available",
    },
    {
        "name": "City Centre Executive",
        "city": "Manchester",
        "bedrooms": 2,
        "max_guests": 4,
        "nightly_rate": 145.00,
        "status": "available",
    },
    {
        "name": "Canary Wharf Residence",
        "city": "London",
        "bedrooms": 2,
        "max_guests": 4,
        "nightly_rate": 210.00,
        "status": "available",
    },
    {
        "name": "Birmingham Grand Apartment",
        "city": "Birmingham",
        "bedrooms": 3,
        "max_guests": 6,
        "nightly_rate": 175.00,
        "status": "available",
    },
    {
        "name": "Leeds Serviced Suite",
        "city": "Leeds",
        "bedrooms": 1,
        "max_guests": 2,
        "nightly_rate": 85.00,
        "status": "maintenance",
    },
]



def seed_database():
    db = SessionLocal()

    try:
        existing_apartments = db.query(Apartment).count()

        if existing_apartments > 0:
            print("Database already contains apartments.")
            return

        for apartment_data in apartments:
            apartment = Apartment(**apartment_data)
            db.add(apartment)

        db.commit()
        print(f"Successfully seeded {len(apartments)} apartments.")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
