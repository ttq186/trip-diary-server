from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import models
import schemas
import crud
import exceptions
from api.v1 import deps


router = APIRouter(prefix="/trips", tags=["Locations"])


@router.get("/{trip_id}/locations", response_model=list[schemas.LocationOut])
async def get_locations(
    trip_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    trip = crud.trip.get(db, id=trip_id)
    if trip is None:
        raise exceptions.ResourceNotFound(resource_type="Trip", id=trip_id)

    locations = crud.location.get_multi_by_trip_id(db, trip_id=trip_id)
    return locations


@router.get("/{trip_id}/locations/{location_id}", response_model=schemas.LocationOut)
async def get_location(
    trip_id: int,
    location_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    trip = crud.trip.get(db, id=trip_id)
    if trip is None:
        raise exceptions.ResourceNotFound(resource_type="Trip", id=trip_id)

    location = crud.location.get(db, id=location_id)
    if location is None:
        raise exceptions.ResourceNotFound(resource_type="Location", id=location_id)
    if location.trip_id != trip_id:
        raise exceptions.NotAuthorized()  # ???
    return location


@router.post("/{trip_id}/locations", response_model=schemas.LocationOut)
async def create_location(
    trip_id: int,
    location_in: schemas.LocationCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    trip = crud.trip.get(db, id=trip_id)
    if trip is None:
        raise exceptions.ResourceNotFound(resource_type="Trip", id=trip_id)
    if trip.user_id != current_user.id:
        raise exceptions.NotAuthorized()
    location_in.trip_id = trip_id
    location_in.user_id = current_user.id
    location = crud.location.create(db, obj_in=location_in)
    return location


@router.put("/{trip_id}/locations/{location_id}", response_model=schemas.LocationOut)
async def update_location(
    trip_id: int,
    location_id: int,
    location_in: schemas.LocationUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    trip = crud.trip.get(db, id=trip_id)
    if trip is None:
        raise exceptions.ResourceNotFound(resource_type="Trip", id=trip_id)
    if trip.user_id != current_user.id:
        raise exceptions.NotAuthorized()

    location = crud.location.get(db, id=location_id)
    if location is None:
        raise exceptions.ResourceNotFound(resource_type="Location", id=location_id)
    if location.trip_id != trip_id:
        raise exceptions.NotAuthorized()  # ???

    location_in = location_in.dict(exclude={"id", "trip_id"})
    location = crud.location.update(db, db_obj=location, obj_in=location_in)
    return location


@router.delete(
    "/{trip_id}/locations/{location_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_location(
    trip_id: int,
    location_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    trip = crud.trip.get(db, id=trip_id)
    if trip is None:
        raise exceptions.ResourceNotFound(resource_type="Trip", id=trip_id)
    if trip.user_id != current_user.id:
        raise exceptions.NotAuthorized()

    location = crud.location.get(db, id=location_id)
    if location is None:
        raise exceptions.ResourceNotFound(resource_type="Location", id=location_id)
    if location.trip_id != trip_id:
        raise exceptions.NotAuthorized()  # ???

    location = crud.location.remove(db, id=location_id)
    return location
