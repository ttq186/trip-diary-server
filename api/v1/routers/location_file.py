from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session

import models
import schemas
import crud
import exceptions
from api.v1 import deps


router = APIRouter(prefix="/trips", tags=["Location Files"])


@router.get(
    "/{trip_id}/locations/{location_id}/files",
    response_model=list[schemas.LocationFileOut],
)
async def get_location_files(
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
    location_files = crud.location_file.get_multi_by_location_id(
        db, location_id=location_id
    )
    return location_files


@router.get(
    "/{trip_id}/locations/{location_id}/files/{file_id}",
    response_model=schemas.LocationFileOut,
)
async def get_location_file(
    trip_id: int,
    location_id: int,
    file_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    location_file = crud.location_file.get(db, id=file_id)
    if location_file is None:
        raise exceptions.ResourceNotFound(resource_type="Location File", id=file_id)
    if location_file.location_id != location_id:
        raise exceptions.NotAuthorized()

    location = crud.location.get(db, id=location_id)
    if location is None:
        raise exceptions.ResourceNotFound(resource_type="Location", id=location_id)
    if location.trip_id != trip_id:
        raise exceptions.NotAuthorized()
    return location_file


@router.post(
    "/{trip_id}/locations/{location_id}/files",
    response_model=schemas.LocationFileOut,
)
async def create_location_file(
    trip_id: int,
    location_id: int,
    location_file_in: schemas.LocationFileCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    location = crud.location.get(db, id=location_id)
    if location is None:
        raise exceptions.ResourceNotFound(resource_type="Location", id=location_id)
    if location.trip_id != trip_id or location.user_id != current_user.id:
        raise exceptions.NotAuthorized()
    location_file_in.location_id = location_id
    location_file = crud.location_file.create(db, obj_in=location_file_in)
    return location_file


@router.delete(
    "/{trip_id}/locations/{location_id}/files/{file_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def delete_location_file(
    trip_id: int,
    location_id: int,
    file_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    location_file = crud.location_file.get(db, id=file_id)
    if location_file is None:
        raise exceptions.ResourceNotFound(resource_type="Location File", id=file_id)
    if location_file.location_id != location_id:
        raise exceptions.NotAuthorized()

    location = crud.location.get(db, id=location_id)
    if location is None:
        raise exceptions.ResourceNotFound(resource_type="Location", id=location_id)
    if location.trip_id != trip_id:
        raise exceptions.NotAuthorized()
    crud.location_file.remove(db, id=file_id)
