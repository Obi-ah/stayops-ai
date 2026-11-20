from sqlalchemy import CheckConstraint, Column, Date, ForeignKey, Integer, Numeric, String

from app.database.base import Base


class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (
    CheckConstraint("check_out > check_in", name="valid_booking_dates"),
    CheckConstraint("number_of_guests > 0", name="positive_guest_count"),
    CheckConstraint("total_price >= 0", name="non_negative_price"),
)

    id = Column(Integer, primary_key=True)
    apartment_id = Column(Integer, ForeignKey("apartments.id"), nullable=False)
    guest_id = Column(Integer, ForeignKey("guests.id"), nullable=False)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    number_of_guests = Column(Integer, nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), nullable=False, default="confirmed")
