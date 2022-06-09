from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session

import schemas
import models
import crud
import exceptions
from core.config import settings
from worker import remind_trip
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

    start_date = str(trip.start_at).split(" ")[0]
    remind_link = f"{settings.BASE_URL}/trips/{trip.id}/remind-again"

    # For prod:
    # time_delta = trip.start_at.days() - trip.created_at.days()
    # task_countdown_seconds = timedelta(
    #     days=trip.start_at.days - (1 if time_delta != 1 else 0.5)
    # )
    task_countdown_seconds = 30  # For demo
    remind_trip.apply_async(
        (current_user.email, start_date, remind_link), countdown=task_countdown_seconds
    )
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
    trip_in = trip_in.dict(exclude={"id", "user_id"}, exclude_unset=True)

    trip = crud.trip.update(db, db_obj=trip, obj_in=trip_in)
    return trip


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
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
    crud.trip.remove(db, id=id)


@router.post("/{id}/remind-again", response_model=schemas.TripOut)
async def remind_trip_again(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    """Remind the upcoming trip again after the first reminder 6 hours."""
    trip = crud.trip.get(db, id=id)
    if trip is None:
        raise exceptions.ResourceNotFound(resource_type="Trip", id=id)
    if not trip.can_be_reminded:
        raise exceptions.TripCantBeReminded()

    start_date = str(trip.start_at).split(" ")[0]

    # For prod:
    # time_delta = trip.start_at.days() - trip.created_at.days()
    # task_countdown_seconds = timedelta(
    #     days=trip.start_at.days - (0.75 if time_delta != 1 else 0.5)
    # )
    task_countdown_seconds = 30  # For demo
    remind_trip.apply_async(
        (current_user.email, start_date), countdown=task_countdown_seconds
    )
    trip = crud.trip.update(db, db_obj=trip, obj_in={"can_be_reminded": False})
    return trip
