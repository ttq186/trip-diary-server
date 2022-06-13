from sqlalchemy.orm import Session

from schemas import TripCreate, TripUpdate, TripScope, TripType
from models import Trip
from crud.base import CRUDBase


class CRUDTrip(CRUDBase[Trip, TripCreate, TripUpdate]):
    def get_multi(
        self,
        db: Session,
        *,
        user_id: str | None = None,
        trip_type: TripType = TripType.ALL,
        trip_scope: TripScope = TripScope.ALL,
        skip: int = 0,
        limit: int | None = None
    ) -> list[Trip]:
        stmt = db.query(Trip)
        if user_id is not None:
            stmt = stmt.filter(Trip.user_id == user_id)
        if trip_type == TripType.AROUND:
            stmt = stmt.filter(Trip.back_trip_at.isnot(None))
        elif trip_type == TripType.SINGLE:
            stmt = stmt.filter(Trip.back_trip_at == None)  # noqa

        trips = stmt.offset(skip).limit(limit).all()
        return trips


trip = CRUDTrip(Trip)
