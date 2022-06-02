from datetime import datetime

from pydantic import EmailStr

from schemas import CamelModel


class UserBase(CamelModel):
    """Shared properties."""

    id: str | None = None
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    avatar_url: str | None = None
    cover_img_url: str | None = None
    is_female: bool | None = None
    description: str | None = None
    country: str | None = None
    date_of_birth: datetime | None = None
    created_at: datetime | None = None


class UserCreate(UserBase):
    """Properties to receive via Create endpoint."""

    email: EmailStr
    password: str

    class Config:
        exclude = ["id"]


class UserUpdate(UserBase):
    """Properties to receive via Update endpoint."""

    password: str | None = None

    class Config:
        exclude = ["id"]


class UserForgotPassword(CamelModel):
    email: EmailStr


class UserResetPassword(CamelModel):
    password: str


class UserInDbBase(UserBase):
    class Config:
        orm_mode = True


class UserInDb(UserInDbBase):
    """Additional properties stored in DB."""

    password: str


class UserOut(UserInDbBase):
    """Properties to return to client."""

    is_admin: bool = False


class UserBlobSASOut(CamelModel):
    sas_token: str
