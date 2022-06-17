from enum import Enum
from datetime import datetime

from schemas import CamelModel


class FileType(Enum):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    COMPRESS = "COMPRESS"


class LocationFileBase(CamelModel):
    """Shared properties."""

    url: str | None = None
    type: FileType = FileType.IMAGE
    uploaded_at: datetime | None = None
    location_id: int | None = None


class LocationFileCreate(LocationFileBase):
    """Properties to receive via Create endpoint."""

    url: str


class LocationFileUpdate(LocationFileBase):
    """Properties to receive via Update endpoint."""

    pass


class LocationFileOut(LocationFileBase):
    id: int

    class Config:
        orm_mode = True
