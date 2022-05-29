from sqlalchemy.orm import Session

from crud.base import CRUDBase
from schemas import TripCreate, TripUpdate
from models import TripLike


class CRUDTripLike(CRUDBase[TripLike, TripCreate, TripUpdate]):
    def get_by_trip_id(
        self, trip_id: int, db: Session, skip: int = 0, limit: int | None = None
    ) -> list[TripLike]:
        trip_likes = (
            db.query(TripLike)
            .filter_by(trip_id=trip_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return trip_likes


trip_like = CRUDTripLike(TripLike)
