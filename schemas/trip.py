from datetime import date

from schemas import CamelModel
from schemas.location import LocationOut


class TripBase(CamelModel):
    """Shared properties."""

    id: int | None = None
    name: str | None = None
    description: str | None = None
    cover_img_url: str | None = None
    from_lat: float | None = None
    from_lng: float | None = None
    to_lat: float | None = None
    to_lng: float | None = None
    start_at: date | None = None
    finish_at: date | None = None
    back_trip_at: date | None = None
    is_public: bool | None = None
    locations: list[LocationOut] | None = None
    user_id: str | None = None


class TripCreate(TripBase):
    """Properties to receive via Create endpoint."""

    name: str
    from_lat: float
    from_lng: float
    to_lat: float
    to_lng: float
    start_at: date
    finish_at: date
    is_public: bool = True

    class Config:
        exclude = ["id"]


class TripUpdate(TripBase):
    """Properties to receive via Update endpoint."""

    class Config:
        exclude = ["id", "user_id"]


class TripInDBBase(TripBase):
    class Config:
        orm_mode = True


class TripInDB(TripInDBBase):
    pass


class TripOut(TripInDB):
    """Properties to return to client."""

    locations: list[LocationOut]
