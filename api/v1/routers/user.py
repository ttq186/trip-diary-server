from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, status, Response
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from azure.storage.blob import (
    generate_account_sas,
    AccountSasPermissions,
    ResourceTypes,
)

from api.v1 import deps
from core import security
from core.config import settings
from worker import send_verify_account_email
import crud
import exceptions
import schemas
import models
import utils

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/blob-sas", response_model=schemas.UserBlobSASOut)
async def get_blob_sas(current_user: models.User = Depends(deps.get_current_user)):
    sas_token = generate_account_sas(
        account_name=settings.AZURE_STORAGE_ACCOUNT_NAME,
        resource_types=ResourceTypes(object=True),
        account_key=settings.AZURE_ACCESS_KEY,
        permission=AccountSasPermissions(
            read=True, write=True, create=True, update=True
        ),
        expiry=datetime.now() + timedelta(hours=12),
    )
    return schemas.UserBlobSASOut(sas_token=sas_token)


@router.post("/{id}/verify/{token}")
async def verify_user(id: str, token: str, db: Session = Depends(deps.get_db)):
    user = crud.user.get(db, id=id)
    if user is None:
        raise exceptions.ResourceNotFound(resource_type="User", id=id)
    if user.is_verified:
        raise exceptions.AccountHasBeenVerified()

    token_data = security.decode_jwt_token(token)
    if token_data is None:
        raise exceptions.VerifyLinkHasExpired()
    user = crud.user.update(db, db_obj=user, obj_in={"is_verified": True})
    return {"detail": "Verify account successfully!"}


@router.get("", response_model=list[schemas.UserOut])
async def get_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int | None = None,
    current_user: models.User = Depends(deps.get_current_user),
):
    """Retrieve users."""
    if current_user.is_admin:
        users = crud.user.get_multi(db, skip=skip, limit=limit)
    else:
        users = crud.user.get(db, id=current_user.id)
        users = [users]
    return users


@router.get("/me", response_model=schemas.UserOut)
async def get_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    return current_user


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


@router.post("", status_code=status.HTTP_201_CREATED)
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
    if user_in.password is not None:
        user_in.password = security.get_hashed_password(user_in.password)
    new_user = crud.user.create(db, obj_in=user_in)

    verify_token = security.create_access_token(
        {"id": new_user_id}, expires_delta=timedelta(minutes=15)
    )
    verify_link = f"{settings.BASE_URL}/users/{new_user_id}/verify/{verify_token}"
    send_verify_account_email.apply_async((new_user.email, verify_link))
    return {"detail": "Sign up successfully!"}


@router.put("/{id}", response_model=schemas.UserOut)
async def update_user(
    id: str,
    user_in: schemas.UserUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    """Update a specific user by id."""
    user = crud.user.get(db, id)
    if user is None:
        raise exceptions.ResourceNotFound(resource_type="User", id=id)
    if not user.is_admin and current_user.id != id:
        raise exceptions.NotAuthorized()

    user_in = user_in.dict(exclude={"id"}, exclude_unset=True)
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_user(
    id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_superuser),
):
    """Remove a specific user by id."""
    user = crud.user.get(db, id)
    if user is None:
        raise exceptions.ResourceNotFound(resource_type="User", id=id)
    crud.user.remove(db, id=id)


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
    reset_link = f"{settings.BASE_URL}/reset-password/{user.id}/{reset_token}"
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
