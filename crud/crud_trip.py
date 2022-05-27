from sqlalchemy.orm import Session

import models
import schemas
from crud.base import CRUDBase


class CRUDTrip(CRUDBase[models.Trip, schemas.TripCreate, schemas.TripUpdate]):
    def get_multi_by_owner(
        user_id: str, db: Session, *, skip: int = 0, limit: int = 10e6
    ) -> list[models.Trip]:
        trips = (
            db.query(models.Trip)
            .filter_by(user_id=user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return trips


trip = CRUDTrip(models.Trip)
