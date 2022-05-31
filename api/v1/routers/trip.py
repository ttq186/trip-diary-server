from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import schemas
import models
import crud
import exceptions
from api.v1 import deps

router = APIRouter(prefix="/trips", tags=["Trips"])


@router.get("", response_model=list[schemas.TripOut])
async def get_trips(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int | None = None,
    current_user: models.User = Depends(deps.get_current_user),
):
    """Retrieve trips by role."""
    if current_user.is_admin:
        trips = crud.trip.get_multi(db, skip=skip, limit=limit)
    else:
        trips = crud.trip.get_multi_by_owner(
            db, skip=skip, limit=limit, user_id=current_user.id
        )
    return trips


@router.get("/{id}", response_model=schemas.TripOut)
async def get_trip(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    """Retrieve a specific trip by id."""
    trip = crud.trip.get(db, id)
    if trip is None:
        raise exceptions.ResourceNotFound(resource_type="Trip", id=id)
    if trip.user_id != current_user.id and (not current_user.is_admin):
        raise exceptions.NotAuthorized()
    return trip


@router.post("", response_model=schemas.TripOut)
async def create_trip(
    trip_in: schemas.TripCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    """Create a new trip."""
    trip_in.user_id = current_user.id
    trip = crud.trip.create(db, trip_in)
    return trip


@router.put("/{id}", response_model=schemas.TripOut)
async def update_trip(
    id: int,
    trip_in: schemas.TripUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    """Update a specific trip by id."""
    trip = crud.trip.get(db, id)
    if trip is None:
        raise exceptions.ResourceNotFound(resource_type="Trip", id=id)
    if trip.user_id != current_user.id and (not current_user.is_admin):
        raise exceptions.NotAuthorized()
    trip_in = trip_in.dict(exclude_unset=True)

    trip = crud.trip.update(db, db_obj=trip, obj_in=trip_in)
    return trip


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trip(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    """Remove a specific trip by id."""
    trip = crud.trip.get(db, id=id)
    if trip is None:
        raise exceptions.ResourceNotFound(resource_type="Trip", id=id)
    if trip.user_id != current_user.id and (not current_user.is_admin):
        raise exceptions.NotAuthorized()
    trip = crud.trip.remove(db, id=id)
    return trip