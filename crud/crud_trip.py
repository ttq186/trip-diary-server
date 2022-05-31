from sqlalchemy.orm import Session

from schemas import TripCreate, TripUpdate
from models import Trip
from crud.base import CRUDBase


class CRUDTrip(CRUDBase[Trip, TripCreate, TripUpdate]):
    def get_multi_by_owner(
        self, db: Session, *, skip: int = 0, limit: int | None = None, user_id: str
    ) -> list[Trip]:
        trips = (
            db.query(self._model)
            .filter_by(user_id=user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return trips


trip = CRUDTrip(Trip)
