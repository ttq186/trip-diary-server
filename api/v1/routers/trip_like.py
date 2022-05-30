from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.v1 import deps
import crud
import schemas
import models
import exceptions


router = APIRouter(prefix="/trip_likes", tags=["Trip Likes"])


@router.post("/", response_model=schemas.TripLikeOut)
async def create_trip_like_by_trip_id(
    trip_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    trip_like = crud.trip_like.get_by_trip_id(db, trip_id=trip_id)
    if trip_like is None:
        raise exceptions.TripLikeAlreadyMade()

    trip_like_in = {"trip_id": trip_id, "user_id": current_user.id}
    trip = crud.trip_like.create(db, obj_in=trip_like_in)
    return trip


@router.get("/", response_model=list[schemas.TripLikeOut])
async def get_trip_likes(
    trip_id: int | None = None,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    """Retrieve trip likes by trip id or user id."""
    if trip_id is None:
        trip_likes_by_users = crud.trip_like.get_by_user_id(db, user_id=current_user.id)
        return trip_likes_by_users

    trip = crud.trip.get(db, id=trip_id)
    if trip is None:
        raise exceptions.ResourceNotFound(resource_type="Trip", id=trip_id)
    if trip.user_id != current_user.id and (not current_user.is_admin):
        raise exceptions.NotAuthorized()
    trip_likes = crud.trip_like.get_by_trip_id(db, trip_id=trip_id)
    return trip_likes


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_trip_like_by_id(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    trip_like = crud.trip_like.get(db, id=id)
    if trip_like is None:
        raise exceptions.ResourceNotFound(resource_type="Trip Like", id=id)
    if trip_like.user_id != current_user.id and (not current_user.is_admin):
        raise exceptions.NotAuthorized()
    trip_like = crud.trip_like.remove(db, id=id)
    return trip_like


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def remove_trip_like_by_trip_id(
    trip_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    trip_like = crud.trip_like.get_by_trip_id_and_user_id(
        db, trip_id=trip_id, user_id=current_user.id
    )
    if trip_like is None:
        raise exceptions.TripLikeHasNotBeenMade()
    trip_like = crud.trip_like.remove(db, id=trip_like.id)
    return trip_like
