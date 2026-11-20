from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class BookingCreate(BaseModel):
    apartment_id: int = Field(gt=0)
    guest_id: int = Field(gt=0)
    check_in: date
    check_out: date
    number_of_guests: int = Field(gt=0)

    @model_validator(mode="after")
    def check_date_order(self):
        if self.check_out <= self.check_in:
            raise ValueError("check_out must be after check_in")
        return self


class BookingResponse(BookingCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    total_price: Decimal
    status: Literal["confirmed", "cancelled"]
