from datetime import datetime

from schemas import CamelModel


class LocationImageBase(CamelModel):
    """Shared properties."""

    url: str | None = None
    uploaded_at: datetime | None = None
    location_id: int | None = None


class LocationImageCreate(LocationImageBase):
    """Properties to receive via Create endpoint."""

    url: str


class LocationImageUpdate(LocationImageBase):
    """Properties to receive via Update endpoint."""

    pass


class LocationImageInDbBase(LocationImageBase):
    class Config:
        orm_mode = True


class LocationImageInDb(LocationImageInDbBase):
    pass


class LocationImageOut(LocationImageInDbBase):
    id: int
