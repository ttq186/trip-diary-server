from sqlalchemy.orm import Session

from crud.base import CRUDBase
from schemas import TripCreate, TripUpdate
from models import TripLike


class CRUDTripLike(CRUDBase[TripLike, TripCreate, TripUpdate]):
    def get_by_trip_id(
        self, db: Session, trip_id: int, skip: int = 0, limit: int | None = None
    ) -> list[TripLike]:
        trip_likes = (
            db.query(TripLike)
            .filter_by(trip_id=trip_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return trip_likes

    def get_by_user_id(
        self, db: Session, user_id: int, skip: int = 0, limit: int | None = None
    ) -> list[TripLike]:
        trip_likes = (
            db.query(TripLike)
            .filter_by(user_id=user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return trip_likes

    def get_by_trip_id_and_user_id(
        self, db: Session, trip_id: int, user_id: str
    ) -> TripLike | None:
        trip_like = (
            db.query(TripLike).filter_by(trip_id=trip_id, user_id=user_id).first()
        )
        return trip_like


trip_like = CRUDTripLike(TripLike)
