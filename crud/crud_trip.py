from sqlalchemy.orm import Session
from models.user import User

from schemas import TripCreate, TripUpdate, TripScope, TripType
from models import Trip
from crud.base import CRUDBase


class CRUDTrip(CRUDBase[Trip, TripCreate, TripUpdate]):
    def get_multi(
        self,
        db: Session,
        trip_type: TripType | None = None,
        trip_scope: TripScope | None = None,
        skip: int = 0,
        limit: int | None = None,
        search: str | None = None,
        user_id: str | None = None,
    ) -> list[Trip]:
        stmt = db.query(Trip).join(User)
        if user_id is not None:
            stmt = stmt.filter(Trip.user_id == user_id)

        if trip_scope is not None:
            stmt = stmt.filter(Trip.scope == trip_scope)

        if trip_type == TripType.AROUND:
            stmt = stmt.filter(Trip.back_trip_at.isnot(None))
        elif trip_type == TripType.SINGLE:
            stmt = stmt.filter(Trip.back_trip_at == None)  # noqa

        if search is not None:
            stmt = stmt.filter(
                Trip.name.ilike(f"%{search}%")
                | Trip.author_email.ilike(f"%{search}%")
                | Trip.author_username.ilike(f"%{search}%")
                | Trip.author_first_name.ilike(f"%{search}%")
                | Trip.author_last_name.ilike(f"%{search}%")
            )
        trips = stmt.offset(skip).limit(limit).all()
        return trips


trip = CRUDTrip(Trip)
