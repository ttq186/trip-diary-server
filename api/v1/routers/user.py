from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from api.v1 import deps
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
    db: Session = Depends(deps.get_current_user),
    current_user: models.User = Depends(deps.get_current_user),
):
    user = crud.user.get(db, id)
    if user is None:
        raise exceptions.ResourceNotFound(resource_type="User", id=id)
    if not user.is_admin and current_user.id != id:
        raise exceptions.NotAuthorized()

    current_user_data = jsonable_encoder(user)
    update_data = {**current_user_data, **payload.dict(exclude_unset=True)}
    user_in = schemas.UserUpdate(update_data)
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(
    id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_superuser),
):
    user = crud.user.get(db, id)
    if user is None:
        raise exceptions.ResourceNotFound(resource_type="User", id=id)
    user = crud.user.remove(db, id=id)
    return user
