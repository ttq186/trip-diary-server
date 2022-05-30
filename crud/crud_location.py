from sqlalchemy.orm import Session

from crud.base import CRUDBase
from schemas import LocationCreate, LocationUpdate
from models import Location


class CRUDLocation(CRUDBase[Location, LocationCreate, LocationUpdate]):
    def get_multi_by_trip_id(
        self, db: Session, trip_id: int, skip: int = 0, limit: int | None = None
    ) -> list[Location]:
        locations = (
            db.query(Location)
            .filter_by(trip_id=trip_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return locations


location = CRUDLocation(Location)
