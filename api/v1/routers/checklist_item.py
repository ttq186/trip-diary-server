from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import models
import schemas
import crud
import exceptions
from api.v1 import deps


router = APIRouter(prefix="/trips", tags=["Check List Items"])


@router.get("/{trip_id}/checklist", response_model=list[schemas.CheckListItemOut])
async def get_checklist(
    trip_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    trip = crud.trip.get(db, id=trip_id)
    if trip is None:
        raise exceptions.ResourceNotFound(resource_type="Trip", id=trip_id)

    checklist = crud.checklist_item.get_multi_by_trip_id(db, trip_id=trip_id)
    return checklist


@router.get("/{trip_id}/checklist/{item_id}", response_model=schemas.CheckListItemOut)
async def get_checklist_item(
    trip_id: int,
    item_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    trip = crud.trip.get(db, id=trip_id)
    if trip is None:
        raise exceptions.ResourceNotFound(resource_type="Trip", id=trip_id)

    checklist_item = crud.checklist_item.get(db, id=item_id)
    if checklist_item is None:
        raise exceptions.ResourceNotFound(resource_type="Checklist Item", id=item_id)
    if checklist_item.trip_id != trip_id:
        raise exceptions.NotAuthorized()  # ???
    return checklist_item


@router.post("/{trip_id}/checklist", response_model=schemas.CheckListItemOut)
async def create_checklist_item(
    trip_id: int,
    checklist_item_in: schemas.CheckListItemCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    trip = crud.trip.get(db, id=trip_id)
    if trip is None:
        raise exceptions.ResourceNotFound(resource_type="Trip", id=trip_id)
    if trip.user_id != current_user.id:
        raise exceptions.NotAuthorized()
    checklist_item_in.trip_id = trip_id
    checklist_item = crud.checklist_item.create(db, obj_in=checklist_item_in)
    return checklist_item


@router.put("/{trip_id}/checklist/{item_id}", response_model=schemas.CheckListItemOut)
async def update_checklist_item(
    trip_id: int,
    item_id: int,
    checklist_item_in: schemas.CheckListItemUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    trip = crud.trip.get(db, id=trip_id)
    if trip is None:
        raise exceptions.ResourceNotFound(resource_type="Trip", id=trip_id)
    if trip.user_id != current_user.id:
        raise exceptions.NotAuthorized()

    checklist_item = crud.checklist_item.get(db, id=item_id)
    if checklist_item is None:
        raise exceptions.ResourceNotFound(resource_type="Checklist Item", id=item_id)
    if checklist_item.trip_id != trip_id:
        raise exceptions.NotAuthorized()  # ???

    checklist_item = crud.checklist_item.update(
        db, db_obj=checklist_item, obj_in=checklist_item_in
    )
    return checklist_item


@router.delete("/{trip_id}/checklist/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_checklist_item(
    trip_id: int,
    item_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    trip = crud.trip.get(db, id=trip_id)
    if trip is None:
        raise exceptions.ResourceNotFound(resource_type="Trip", id=trip_id)
    if trip.user_id != current_user.id:
        raise exceptions.NotAuthorized()

    checklist_item = crud.checklist_item.get(db, id=item_id)
    if checklist_item is None:
        raise exceptions.ResourceNotFound(resource_type="Checklist Item", id=item_id)
    if checklist_item.trip_id != trip_id:
        raise exceptions.NotAuthorized()  # ???

    checklist_item = crud.checklist_item.remove(db, id=item_id)
    return checklist_item
