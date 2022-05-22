from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from api.v1 import deps
import crud
import exceptions
import schemas
import models
import utils

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/", response_model=list[schemas.UserOut] | schemas.UserOut)
async def get_users(
    db: Session = Depends(deps.get_db),
    skip: int | None = 0,
    limit: int | None = 10e6,
    current_user: models.User = Depends(deps.get_current_user),
):
    if current_user.is_admin:
        users = crud.user.get_multi(db, skip=skip, limit=limit)
    else:
        users = db.query(models.User).filter_by(id=current_user.id).first()
    return users


@router.get("/{id}", response_model=schemas.UserOut | None)
async def get_user(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    if not current_user.is_admin and current_user.id != id:
        raise exceptions.NotAuthorized()
    user = crud.user.get(db, id=id)
    if user is None:
        raise exceptions.ResourceNotFound(resource_type="User", id=id)
    return user


@router.create("/", response_model=schemas.UserOut)
async def create_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(deps.get_db),
):
    user = crud.user.get_by_email(db, email=user_in.get("email"))
    if user is not None:
        raise exceptions.EmailAlreadyExists()

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
    current_user: models.User = Depends(deps.get_current_superuser),
):
    """Update a specific user."""
    user = crud.user.get(db, id=id)
    if user is None:
        raise exceptions.ResourceNotFound(resource_type="User", id=id)

    user_data = jsonable_encoder(user)
    update_data = {**user_data, **payload.dict(exclude_unset=True, exclude={"id"})}
    user_in = schemas.UserUpdate(**update_data)
    updated_user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return updated_user
