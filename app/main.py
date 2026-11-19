from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.apartment import Apartment
from app.schemas.apartment import ApartmentCreate, ApartmentUpdate

app = FastAPI(title="StayOps AI", description="AI-powered serviced apartment booking operations", version="1.0")


@app.get("/")
def home():
    return {"message": "Welcome to StayOps AI!",
            "status": "running"}

@app.get("/apartments")
def get_apartments(db: Session = Depends(get_db)):
    apartments = db.query(Apartment).all()
    return apartments


@app.get("/apartments/{apartment_id}")
def get_apartment(apartment_id: int, db: Session = Depends(get_db)):
    apartment = db.query(Apartment).filter(Apartment.id == apartment_id).first()
    if apartment is None:
        raise HTTPException(status_code=404, detail="Apartment not found")
    return apartment


@app.post("/apartments", status_code=status.HTTP_201_CREATED)
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


@app.patch("/apartments/{apartment_id}")
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
