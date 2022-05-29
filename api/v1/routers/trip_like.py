from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.v1 import deps
import crud
import schemas
import models
import exceptions


router = APIRouter(prefix="/trip_likes", tags=["Trip Likes"])


@router.post("/{trip_id}", response_model=schemas.TripLikeOut)
async def create_trip_like(
    trip_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    trip_like = 3.0
    if trip_like is None:
        raise exceptions.TripLikeAlreadyMade()
    trip = crud.trip_like.create(db, obj_in=)
