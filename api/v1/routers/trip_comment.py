from datetime import datetime

from fastapi import APIRouter, status, Depends, Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import schemas
import models
import crud
import exceptions
from api.v1 import deps

router = APIRouter(prefix="/trips/{trip_id}/comments", tags=["Comments"])


@router.get("", response_model=list[schemas.TripCommentOut])
async def get_comments(
    trip_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    trip = crud.trip.get(db, id=trip_id)
    if trip is None:
        raise exceptions.ResourceNotFound(resource_type="Trip", id=trip_id)
    trip_comments = crud.trip_comment.get_multi_by_trip_id(db, trip_id=trip_id)
    trip_comments_out = []
    for comment in trip_comments:
        if current_user.id in comment.liked_by_users_with_id:
            comment = schemas.TripCommentOut(
                **jsonable_encoder(comment),
                author=comment.author,
                has_liked=True,
                num_of_likes=comment.num_of_likes
            )
        trip_comments_out.append(comment)
    return trip_comments_out


@router.get("/{comment_id}", response_model=schemas.TripCommentOut)
async def get_comment(
    trip_id: int,
    comment_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    trip = crud.trip.get(db, id=trip_id)
    if trip is None:
        raise exceptions.ResourceNotFound(resource_type="Trip", id=trip_id)

    trip_comment = crud.trip_comment.get(db, id=comment_id)
    if trip_comment is None:
        raise exceptions.ResourceNotFound(resource_type="Comment", id=comment_id)
    return trip_comment


@router.post("", response_model=schemas.TripCommentOut)
async def create_comment(
    trip_id: int,
    trip_comment_in: schemas.TripCommentCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    trip = crud.trip.get(db, id=trip_id)
    if trip is None:
        raise exceptions.ResourceNotFound(resource_type="Trip", id=trip_id)
    # if trip.id != trip_id or trip.user_id != current_user.id:
    #     raise exceptions.NotAuthorized()

    trip_comment_in.trip_id = trip_id
    trip_comment_in.user_id = current_user.id
    trip_comment = crud.trip_comment.create(db, obj_in=trip_comment_in)
    return trip_comment


@router.put("/{comment_id}", response_model=schemas.TripCommentOut)
async def update_comment(
    trip_id: int,
    comment_id: int,
    trip_comment_in: schemas.TripCommentUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    trip = crud.trip.get(db, id=trip_id)
    if trip is None:
        raise exceptions.ResourceNotFound(resource_type="Trip", id=trip_id)

    trip_comment = crud.trip_comment.get(db, id=comment_id)
    if trip_comment is None:
        raise exceptions.ResourceNotFound(resource_type="Comment", id=comment_id)
    if trip_comment.trip_id != trip_id or trip_comment.user_id != current_user.id:
        raise exceptions.NotAuthorized()  # ???
    trip_comment_in.updated_at = datetime.now()
    trip_comment = crud.trip_comment.update(
        db, db_obj=trip_comment, obj_in=trip_comment_in
    )
    return trip_comment


@router.delete(
    "/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def delete_comment(
    trip_id: int,
    comment_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    trip = crud.trip.get(db, id=trip_id)
    if trip is None:
        raise exceptions.ResourceNotFound(resource_type="Trip", id=trip_id)

    trip_comment = crud.trip_comment.get(db, id=comment_id)
    if trip_comment is None:
        raise exceptions.ResourceNotFound(resource_type="Comment", id=comment_id)
    if trip_comment.trip_id != trip_id:
        raise exceptions.NotAuthorized()
    crud.trip_comment.remove(db, id=comment_id)
