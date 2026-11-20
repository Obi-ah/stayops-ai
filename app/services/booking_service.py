from sqlalchemy.orm import Session

from app.models.booking import Booking


def check_availability(
    db: Session,
    apartment_id: int,
    check_in,
    check_out
) -> bool:

    conflicting_booking = db.query(Booking).filter(
        Booking.apartment_id == apartment_id,
        Booking.status == "confirmed",
        Booking.check_in < check_out,
        Booking.check_out > check_in,
    ).first()

    return conflicting_booking is None