from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session

from api.v1 import deps
import crud
import schemas
import models
import exceptions


router = APIRouter(prefix="/trips/{trip_id}/likes", tags=["Likes"])


@router.get("", response_model=list[schemas.TripLikeOut])
async def get_likes(
    trip_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    trip = crud.trip.get(db, id=trip_id)
    if trip is None:
        raise exceptions.ResourceNotFound(resource_type="Trip", id=trip_id)
    # if trip.user_id != current_user.id:
    #     raise exceptions.NotAuthorized()

    trip_likes = crud.trip_like.get_multi_by_trip_id(db, trip_id=trip_id)
    return trip_likes


@router.post("", response_model=schemas.TripLikeOut)
async def create_like(
    trip_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    """Retrieve trip likes by trip id or user id."""
    trip = crud.trip.get(db, id=trip_id)
    if trip is None:
        raise exceptions.ResourceNotFound(resource_type="Trip", id=trip_id)
    # if trip.user_id != current_user.id:
    #     raise exceptions.NotAuthorized()

    trip_like = crud.trip_like.get_by_trip_id_and_user_id(
        db, trip_id=trip_id, user_id=current_user.id
    )
    if trip_like is not None:
        raise exceptions.LikeAlreadyMade(resource_type="Trip")

    trip_like_in = schemas.TripLikeCreate(trip_id=trip_id, user_id=current_user.id)
    trip_like = crud.trip_like.create(db, obj_in=trip_like_in)
    return trip_like


@router.delete("", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_like(
    trip_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    trip = crud.trip.get(db, id=trip_id)
    if trip is None:
        raise exceptions.ResourceNotFound(resource_type="Trip", id=trip_id)
    # if trip.user_id != current_user.id:
    #     raise exceptions.NotAuthorized()

    trip_like = crud.trip_like.get_by_trip_id_and_user_id(
        db, trip_id=trip_id, user_id=current_user.id
    )
    if trip_like is None:
        raise exceptions.LikeHasNotBeenMade(resource_type="Trip")
    crud.trip_like.remove(db, id=trip_like.id)
