from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session

from api.v1 import deps
import crud
import schemas
import models
import exceptions


router = APIRouter(
    prefix="/trips/{trip_id}/comments/{comment_id}/likes", tags=["Comment Likes"]
)


@router.get("", response_model=list[schemas.CommentLikeOut])
async def get_likes(
    trip_id: int,
    comment_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    comment = crud.trip_comment.get(db, id=comment_id)
    if comment is None:
        raise exceptions.ResourceNotFound(resource_type="Comment", id=comment_id)
    # if comment.user_id != current_user.id:
    #     raise exceptions.NotAuthorized()

    trip = crud.trip.get(db, id=trip_id)
    if trip is None:
        raise exceptions.ResourceNotFound(resource_type="Trip", id=trip_id)

    comment_likes = crud.comment_like.get_multi_by_comment_id(db, comment_id=comment_id)
    return comment_likes


@router.post("", response_model=schemas.CommentLikeOut)
async def create_like(
    trip_id: int,
    comment_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    comment = crud.trip_comment.get(db, id=comment_id)
    if comment is None:
        raise exceptions.ResourceNotFound(resource_type="Comment", id=comment_id)
    # if comment.user_id != current_user.id:
    #     raise exceptions.NotAuthorized()

    trip = crud.trip.get(db, id=trip_id)
    if trip is None:
        raise exceptions.ResourceNotFound(resource_type="Trip", id=trip_id)

    comment_like = crud.comment_like.get_by_comment_id_and_user_id(
        db, comment_id=comment_id, user_id=current_user.id
    )
    if comment_like is not None:
        raise exceptions.LikeAlreadyMade(resource_type="Comment")

    comment_like_in = schemas.CommentLikeCreate(
        comment_id=comment_id, user_id=current_user.id
    )
    comment_like = crud.comment_like.create(db, obj_in=comment_like_in)
    return comment_like


@router.delete("", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_like(
    trip_id: int,
    comment_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    comment = crud.trip_comment.get(db, id=comment_id)
    if comment is None:
        raise exceptions.ResourceNotFound(resource_type="Comment", id=comment_id)
    # if comment.user_id != current_user.id:
    #     raise exceptions.NotAuthorized()

    trip = crud.trip.get(db, id=trip_id)
    if trip is None:
        raise exceptions.ResourceNotFound(resource_type="Trip", id=trip_id)

    comment_like = crud.comment_like.get_by_comment_id_and_user_id(
        db, comment_id=comment_id, user_id=current_user.id
    )
    if comment_like is None:
        raise exceptions.LikeHasNotBeenMade(resource_type="Comment")
    crud.comment_like.remove(db, id=comment_like.id)
