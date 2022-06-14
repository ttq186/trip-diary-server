from enum import Enum
from datetime import date, datetime

from pydantic import validator

from schemas import CamelModel
from .location import LocationOut
from .user import UserOut

class TripType(Enum):
    ALL = "all"
    SINGLE = "single"
    AROUND = "around"


class TripScope(Enum):
    ALL = "all"
    GLOBAL = "global"
    LOCAL = "local"


class TripBase(CamelModel):
    """Shared properties."""

    name: str | None = None
    description: str | None = None
    cover_img_url: str | None = None
    from_lat: float | None = None
    to_lat: float | None = None
    from_lng: float | None = None
    to_lng: float | None = None
    start_at: date | None = None
    back_trip_at: date | None = None
    created_at: datetime | None = None
    is_finished: bool | None = None
    is_public: bool | None = None
    can_be_reminded: bool | None = None
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
    can_be_reminded: bool = True

    @validator("start_at")
    def date_must_be_in_future(cls, v):
        curr_date = date.today()
        if curr_date >= v:
            raise ValueError("Date must in the future")
        return v


class TripUpdate(TripBase):
    """Properties to receive via Update endpoint."""

    @validator("back_trip_at")
    def date_must_be_in_future(cls, v):
        if v is None:
            return v
        curr_date = date.today()
        if curr_date >= v:
            raise ValueError("Date must in the future")
        return v


class TripOut(TripBase):
    """Properties to return to client."""

    id: int
    author: UserOut | None
    num_of_likes: int
    type: TripType = TripType.ALL
    scope: TripScope = TripScope.ALL
    locations: list[LocationOut]

    class Config:
        orm_mode = True
