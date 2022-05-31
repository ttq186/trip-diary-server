from datetime import date

from pydantic import validator

from schemas import CamelModel
from schemas.location import LocationOut


class TripBase(CamelModel):
    """Shared properties."""

    name: str | None = None
    description: str | None = None
    cover_img_url: str | None = None
    from_lat: float | None = None
    from_lng: float | None = None
    to_lat: float | None = None
    to_lng: float | None = None
    start_at: date | None = None
    finish_at: date | None = None
    is_public: bool | None = None
    user_id: str | None = None


class TripCreate(TripBase):
    """Properties to receive via Create endpoint."""

    name: str
    from_lat: float
    from_lng: float
    to_lat: float
    to_lng: float
    start_at: date
    is_public: bool = True

    @validator("start_at")
    def date_must_be_in_future(cls, v):
        curr_date = date.today()
        if curr_date >= v:
            raise ValueError("Date must in the future")
        return v

    class Config:
        exclude = ["id"]


class TripUpdate(TripBase):
    """Properties to receive via Update endpoint."""

    @validator("finish_at")
    def date_must_be_in_future(cls, v):
        if v is None:
            return v
        curr_date = date.today()
        if curr_date >= v:
            raise ValueError("Date must in the future")
        return v


class TripInDBBase(TripBase):
    class Config:
        orm_mode = True


class TripInDB(TripInDBBase):
    pass


class TripOut(TripInDB):
    """Properties to return to client."""

    id: int
    num_of_likes: int
    locations: list[LocationOut]
