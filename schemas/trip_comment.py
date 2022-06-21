from datetime import datetime

from pydantic import EmailStr

from schemas import CamelModel


class TripCommentBase(CamelModel):
    id: int | None = None
    content: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    trip_id: int | None = None
    comment_id: int | None = None


class TripCommentCreate(TripCommentBase):
    user_id: str | None = None
    content: str


class TripCommentUpdate(TripCommentBase):
    user_id: str | None = None


class TripCommentOutBase(TripCommentBase):
    class Config:
        orm_mode = True


class TripCommentAuthorOut(CamelModel):
    id: str | None = None
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None

    class Config:
        orm_mode = True


class TripCommentOut(TripCommentOutBase):
    author: TripCommentAuthorOut
    has_liked: bool = False
    replies: list[TripCommentOutBase] = []
