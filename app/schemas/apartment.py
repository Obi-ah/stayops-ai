from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ApartmentCreate(BaseModel):
    name: str
    city: str
    bedrooms: int = Field(gt=0)
    max_guests: int = Field(gt=0)
    nightly_rate: Decimal = Field(gt=0)
    status: Literal["available", "maintenance", "inactive"] = "available"


class ApartmentUpdate(BaseModel):
    name: str | None = None
    city: str | None = None
    bedrooms: int | None = Field(default=None, gt=0)
    max_guests: int | None = Field(default=None, gt=0)
    nightly_rate: Decimal | None = Field(default=None, gt=0)
    status: Literal["available", "maintenance", "inactive"] | None = None


class ApartmentResponse(ApartmentCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
