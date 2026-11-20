from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.apartment import Apartment
from app.schemas.apartment import ApartmentCreate, ApartmentResponse, ApartmentUpdate

from app.models.guest import Guest
from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingResponse
from app.schemas.guest import GuestCreate, GuestResponse
from app.services.booking_service import check_availability

app = FastAPI(title="StayOps AI", description="AI-powered serviced apartment booking operations", version="1.0")


@app.get("/")
def home():
    return {"message": "Welcome to StayOps AI!",
            "status": "running"}

@app.get("/apartments", response_model=list[ApartmentResponse])
def get_apartments(db: Session = Depends(get_db)):
    apartments = db.query(Apartment).all()
    return apartments


@app.get("/apartments/{apartment_id}", response_model=ApartmentResponse)
def get_apartment(apartment_id: int, db: Session = Depends(get_db)):
    apartment = db.query(Apartment).filter(Apartment.id == apartment_id).first()
    if apartment is None:
        raise HTTPException(status_code=404, detail="Apartment not found")
    return apartment


@app.post("/apartments", response_model=ApartmentResponse, status_code=status.HTTP_201_CREATED)
def create_apartment(apartment_data: ApartmentCreate, db: Session = Depends(get_db)):
    apartment = Apartment(**apartment_data.model_dump())
    db.add(apartment)
    try:
        db.commit()
        db.refresh(apartment)
    except Exception:
        db.rollback()
        raise
    return apartment


@app.patch("/apartments/{apartment_id}", response_model=ApartmentResponse)
def update_apartment(
    apartment_id: int,
    apartment_data: ApartmentUpdate,
    db: Session = Depends(get_db)
):
    apartment = db.query(Apartment).filter(
        Apartment.id == apartment_id
    ).first()

    if apartment is None:
        raise HTTPException(status_code=404, detail="Apartment not found")

    try:
        update_data = apartment_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(apartment, key, value)

        db.commit()
        db.refresh(apartment)
    except Exception:
        db.rollback()
        raise

    return apartment


@app.delete("/apartments/{apartment_id}", status_code=204)
def delete_apartment(apartment_id: int, db: Session = Depends(get_db)):
    apartment = db.query(Apartment).filter(
        Apartment.id == apartment_id
    ).first()

    if apartment is None:
        raise HTTPException(status_code=404, detail="Apartment not found")

    try:
        db.delete(apartment)
        db.commit()
    except Exception:
        db.rollback()
        raise

    return None


@app.post("/bookings", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db)
):
    # 1. Find apartment
    apartment = db.query(Apartment).filter(
        Apartment.id == booking_data.apartment_id
    ).first()

    if apartment is None:
        raise HTTPException(status_code=404, detail="Apartment not found")

    # 2. Check apartment status
    if apartment.status != "available":
        raise HTTPException(
            status_code=400,
            detail="Apartment is not available for booking"
        )

    # 3. Find guest
    guest = db.query(Guest).filter(
        Guest.id == booking_data.guest_id
    ).first()

    if guest is None:
        raise HTTPException(status_code=404, detail="Guest not found")

    # 4. Check guest capacity
    if booking_data.number_of_guests > apartment.max_guests:
        raise HTTPException(
            status_code=400,
            detail="Apartment capacity exceeded"
        )

    # 5. Check date availability
    available = check_availability(
        db,
        apartment.id,
        booking_data.check_in,
        booking_data.check_out
    )

    if not available:
        raise HTTPException(
            status_code=409,
            detail="Apartment is already booked for these dates"
        )

    # 6. Calculate price
    number_of_nights = (
        booking_data.check_out - booking_data.check_in
    ).days

    total_price = apartment.nightly_rate * number_of_nights

    # 7. Create booking
    booking = Booking(
        apartment_id=apartment.id,
        guest_id=guest.id,
        check_in=booking_data.check_in,
        check_out=booking_data.check_out,
        number_of_guests=booking_data.number_of_guests,
        total_price=total_price,
        status="confirmed"
    )

    db.add(booking)

    try:
        db.commit()
        db.refresh(booking)
    except Exception:
        db.rollback()
        raise

    return booking


@app.post("/guests", response_model=GuestResponse, status_code=status.HTTP_201_CREATED)
def create_guest(
    guest_data: GuestCreate,
    db: Session = Depends(get_db)
):
    guest = Guest(**guest_data.model_dump())

    db.add(guest)
    try:
        db.commit()
        db.refresh(guest)
    except Exception:
        db.rollback()
        raise

    return guest
