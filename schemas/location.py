from datetime import date

from schemas import CamelModel


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

    review: str
    lat: float
    lng: float
    start_at: date


class LocationUpdate(LocationBase):
    """Properties to return via Update endpoint."""

    class Config:
        exclude = {"trip_id", "user_id"}


class LocationInDbBase(LocationBase):
    class Config:
        orm_mode = True


class LocationInDb(LocationInDbBase):
    pass


class LocationOut(LocationInDbBase):
    """Properties to retur to client."""

    id: int
