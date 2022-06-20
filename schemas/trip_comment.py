from datetime import datetime

from schemas import CamelModel


class TripCommentBase(CamelModel):
    id: int | None = None
    content: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    trip_id: int | None = None
    user_id: str | None = None
    comment_id: int | None = None


class TripCommentCreate(TripCommentBase):
    content: str


class TripCommentUpdate(TripCommentBase):
    pass


class TripCommentOutBase(TripCommentBase):
    class Config:
        orm_mode = True


class TripCommentOut(TripCommentOutBase):
    replies: list[TripCommentOutBase] = []
