from schemas import CamelModel


class CheckListItemBase(CamelModel):
    """Shared properties."""

    name: str | None = None
    notes: str | None = None
    has_prepared: bool | None = None
    trip_id: int | None = None


class CheckListItemCreate(CheckListItemBase):
    """Properties to reiceive via Create endpoint."""

    name: str


class CheckListItemUpdate(CheckListItemBase):
    """Properties to return via Update endpoint."""


class CheckListItemOut(CheckListItemBase):
    """Properties to retur to client."""

    id: int

    class Config:
        orm_mode = True
