from datetime import date

from pydantic import validator

from schemas import CamelModel
from schemas.location_image import LocationImageOut


class LocationBase(CamelModel):
    """Shared properties."""

    review: str | None = None
    lat: float | None = None
    lng: float | None = None
    start_at: date | None = None
    trip_id: int | None = None
    user_id: str | None = None


class LocationCreate(LocationBase):
    """Properties to reiceive via Create endpoint."""

    lat: float
    lng: float
    start_at: date

    @validator("start_at")
    def date_must_be_in_future(cls, v):
        curr_date = date.today()
        if curr_date >= v:
            raise ValueError("Date must in the future")
        return v


class LocationUpdate(LocationBase):
    """Properties to return via Update endpoint."""


class LocationInDbBase(LocationBase):
    class Config:
        orm_mode = True


class LocationInDb(LocationInDbBase):
    pass


class LocationOut(LocationInDbBase):
    """Properties to retur to client."""

    id: int
    images: list[LocationImageOut]
