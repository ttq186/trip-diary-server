from datetime import datetime

from schemas import CamelModel


class TripBase(CamelModel):
    """Shared properties."""

    name: str
    description: str | None = None
    cover_img_url: str | None = None
    from_lat: float | None = None
    from_lng: float | None = None
    to_lat: float | None = None
    to_lat: float | None = None
    day_count: int | None = None
    departure_at: datetime | None = None
    back_trip_at: datetime | None = None
    is_public: bool | None = None
    user_id: str | None = None


class TripCreate(TripBase):
    """Properties to receive via Create endpoint."""

    name: str
    from_lat: float
    from_lng: float
    to_lat: float
    to_lng: float
    day_count: int
    departure_at: datetime
    back_trip_at: datetime | None
    is_public: bool = True


class TripUpdate(TripBase):
    """Properties to receive via Update endpoint."""

    pass


class TripInDBBase(TripBase):
    class Config:
        orm_mode = True


class TripInDB(TripInDBBase):
    pass


class TripOut(TripInDB):
    """Properties to return to client."""

    pass
