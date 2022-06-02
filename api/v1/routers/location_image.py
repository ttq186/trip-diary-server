from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import models
import schemas
import crud
import exceptions
from api.v1 import deps


router = APIRouter(prefix="/trips", tags=["Location Images"])


@router.get(
    "/{trip_id}/locations/{location_id}/images",
    response_model=list[schemas.LocationImageOut],
)
async def get_location_images(
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
    location_images = crud.location_image.get_multi_by_location_id(
        db, location_id=location_id
    )
    return location_images


@router.get(
    "/{trip_id}/locations/{location_id}/images/{image_id}",
    response_model=schemas.LocationImageOut,
)
async def get_location_image(
    trip_id: int,
    location_id: int,
    image_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    # trip = crud.trip.get(db, id=trip_id)
    # if trip is None:
    #     raise exceptions.ResourceNotFound(resource_type="Trip", id=trip_id)

    # location = crud.location.get(db, id=location_id)
    # if location is None:
    #     raise exceptions.ResourceNotFound(resource_type="Location", id=location_id)

    # location_image = crud.location_image.get(db, id=image_id)
    # if location_image is None:
    #     raise exceptions.ResourceNotFound(resource_type="Location Image", id=image_id)
    # if location_image.location_id != location_id:
    #     raise exceptions.NotAuthorized()
    # return location_image
    location_image = crud.location_image.get(db, id=image_id)
    if location_image is None:
        raise exceptions.ResourceNotFound(resource_type="Location Image", id=image_id)
    if location_image.location_id != location_id:
        raise exceptions.NotAuthorized()

    location = crud.location.get(db, id=location_id)
    if location is None:
        raise exceptions.ResourceNotFound(resource_type="Location", id=location_id)
    if location.trip_id != trip_id:
        raise exceptions.NotAuthorized()
    return location_image


@router.post(
    "/{trip_id}/locations/{location_id}/images",
    response_model=schemas.LocationImageOut,
)
async def create_location_image(
    trip_id: int,
    location_id: int,
    location_image_in: schemas.LocationImageCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    location = crud.location.get(db, id=location_id)
    if location is None:
        raise exceptions.ResourceNotFound(resource_type="Location", id=location_id)
    if location.trip_id != trip_id or location.user_id != current_user.id:
        raise exceptions.NotAuthorized()
    location_image_in.location_id = location_id
    location_image = crud.location_image.create(db, obj_in=location_image_in)
    return location_image


@router.delete(
    "/{trip_id}/locations/{location_id}/images/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_location_image(
    trip_id: int,
    location_id: int,
    image_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    location_image = crud.location_image.get(db, id=image_id)
    if location_image is None:
        raise exceptions.ResourceNotFound(resource_type="Location Image", id=image_id)
    if location_image.location_id != location_id:
        raise exceptions.NotAuthorized()

    location = crud.location.get(db, id=location_id)
    if location is None:
        raise exceptions.ResourceNotFound(resource_type="Location", id=location_id)
    if location.trip_id != trip_id:
        raise exceptions.NotAuthorized()
    location_image = crud.location_image.remove(db, id=image_id)
    return location_image
