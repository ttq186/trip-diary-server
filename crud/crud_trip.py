from sqlalchemy.orm import Session

from schemas import TripCreate, TripUpdate
from models import Trip
from crud.base import CRUDBase


class CRUDTrip(CRUDBase[Trip, TripCreate, TripUpdate]):
    def get_multi(
        self,
        db: Session,
        *,
        is_around: bool = False,
        is_global: bool = False,
        skip: int = 0,
        limit: int | None = None
    ) -> list[Trip]:
        if is_around:
            trips = (
                db.query(Trip)
                .filter(Trip.back_trip_at.isnot(None))
                .offset(skip)
                .limit(limit)
                .all()
            )
        else:
            trips = db.query(Trip).offset(skip).limit(limit).all()
        return trips

    def get_multi_by_owner(
        self,
        db: Session,
        *,
        is_around: bool = False,
        is_global: bool = False,
        skip: int = 0,
        limit: int | None = None,
        user_id: str
    ) -> list[Trip]:
        if is_around:
            trips = (
                db.query(Trip)
                .filter(Trip.back_trip_at.isnot(None), Trip.user_id == user_id)
                .offset(skip)
                .limit(limit)
                .all()
            )
        else:
            trips = (
                db.query(Trip)
                .filter_by(user_id=user_id)
                .offset(skip)
                .limit(limit)
                .all()
            )
        return trips


trip = CRUDTrip(Trip)
