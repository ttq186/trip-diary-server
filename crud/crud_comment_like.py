from sqlalchemy.orm import Session

from crud.base import CRUDBase
from schemas import CommentLikeCreate, CommentLikeUpdate
from models import CommentLike


class CRUDCommentLike(CRUDBase[CommentLike, CommentLikeCreate, CommentLikeUpdate]):
    def get_multi_by_comment_id(
        self, db: Session, comment_id: int, skip: int = 0, limit: int | None = None
    ) -> list[CommentLike]:
        comment_likes = (
            db.query(CommentLike)
            .filter_by(comment_id=comment_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return comment_likes

    def get_by_comment_id_and_user_id(
        self, db: Session, comment_id: int, user_id: str
    ) -> CommentLike | None:
        comment_like = (
            db.query(CommentLike)
            .filter_by(comment_id=comment_id, user_id=user_id)
            .first()
        )
        return comment_like


comment_like = CRUDCommentLike(CommentLike)
