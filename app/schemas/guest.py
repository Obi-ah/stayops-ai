from pydantic import BaseModel, ConfigDict


class GuestCreate(BaseModel):
    full_name: str
    email: str
    phone: str | None = None


class GuestResponse(GuestCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
