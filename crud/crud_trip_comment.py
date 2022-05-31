from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models import TripComment
from schemas import TripCommentCreate, TripCommentUpdate


class CRUDTripComment(CRUDBase[TripComment, TripCommentCreate, TripCommentUpdate]):
    def get_multi_by_trip_id(
        self, db: Session, trip_id: int, skip: int = 0, limit: int | None = None
    ) -> list[TripComment]:
        trip_comments = (
            db.query(TripComment)
            .filter_by(trip_id=trip_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return trip_comments

    def get_by_trip_id_and_user_id(
        self, db: Session, trip_id: int, user_id: str
    ) -> TripComment | None:
        trip_comment = (
            db.query(TripComment).filter_by(trip_id=trip_id, user_id=user_id).first()
        )
        return trip_comment


trip_comment = CRUDTripComment(TripComment)
