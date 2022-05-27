from datetime import timedelta

from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from api.v1 import deps
from core import security
from core.config import settings
import crud
import exceptions
import schemas
import models
import utils

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[schemas.UserOut])
async def get_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 10e6,
    current_user: models.User = Depends(deps.get_current_user),
):
    """Retrieve users."""
    if current_user.is_admin:
        users = crud.user.get_multi(db, skip=skip, limit=limit)
    else:
        users = crud.user.get(db, id=current_user.id)
        users = [users]
    return users


@router.get("/{id}", response_model=schemas.UserOut)
async def get_user(
    id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    """Retrieve a specific user by id."""
    if not current_user.is_admin and current_user.id != id:
        raise exceptions.NotAuthorized()
    user = crud.user.get(db, id=id)
    if user is None:
        raise exceptions.ResourceNotFound(resource_type="User", id=id)
    return user


@router.post("/", response_model=schemas.UserOut)
async def create_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(deps.get_db),
):
    """Create a new user."""
    user = crud.user.get_by_email(db, email=user_in.email)
    if user is not None:
        raise exceptions.EmailAlreadyExists()
    if not utils.is_valid_email(user_in.email):
        raise exceptions.InvalidEmail()

    new_user_id = utils.generate_uuid()
    while crud.user.get(db, id=new_user_id) is not None:
        new_user_id = utils.generate_uuid()
    user_in.id = new_user_id
    new_user = crud.user.create(db, obj_in=user_in)
    return new_user


@router.put("/{id}", response_model=schemas.UserOut)
async def update_user(
    id: str,
    payload: schemas.UserUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    """Update a specific user by id."""
    user = crud.user.get(db, id)
    if user is None:
        raise exceptions.ResourceNotFound(resource_type="User", id=id)
    if not user.is_admin and current_user.id != id:
        raise exceptions.NotAuthorized()

    current_user_data = jsonable_encoder(user)
    update_data = {**current_user_data, **payload.dict(exclude_unset=True)}
    user_in = schemas.UserUpdate(**update_data)
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(
    id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_superuser),
):
    """Remove a specific user by id."""
    user = crud.user.get(db, id)
    if user is None:
        raise exceptions.ResourceNotFound(resource_type="User", id=id)
    user = crud.user.remove(db, id=id)
    return user


@router.post("/forgot-password")
async def forgot_password(
    user_in: schemas.UserForgotPassword, db: Session = Depends(deps.get_db)
):
    """Send reset password email."""
    user = crud.user.get_by_email(db, email=user_in.email)
    if user is None:
        raise exceptions.EmailNotExists()
    if user.password is None:
        raise exceptions.AccountCreatedByGoogle()

    to_encode = {"id": user.id}
    SECRET_KEY = settings.JWT_SECRET_KEY + user.password
    reset_token = security.create_access_token(
        to_encode, timedelta(minutes=15), JWT_SECRET_KEY=SECRET_KEY
    )
    reset_link = (
        f"{settings.PASSWORD_RESET_BASE_URL}/reset-password/{user.id}/{reset_token}"
    )
    utils.send_reset_password_email(to_email=user_in.email, reset_link=reset_link)
    return {"detail": "Password reset requests successfully!"}


@router.post("/reset-password/{id}/{token}")
async def reset_password(
    id: str,
    token: str,
    user_in: schemas.UserResetPassword,
    db: Session = Depends(deps.get_db),
):
    """Reset password."""
    user = crud.user.get(db, id=id)
    if user is None:
        raise exceptions.ResourceNotFound(resource_type="User", id=id)
    try:
        SECRET_KEY = settings.JWT_SECRET_KEY + user.password
        jwt.decode(token, SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if user_in.password is not None:
            user_in.password = security.get_hashed_password(user_in.password)
            user = crud.user.update(db, db_obj=user, obj_in=user_in)
        return {"detail": "Reset password successfully!"}

    except JWTError:
        raise exceptions.ResetLinkExpired()
