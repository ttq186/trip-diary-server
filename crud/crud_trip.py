from sqlalchemy.orm import Session

import models
import schemas
from crud.base import CRUDBase


class CRUDTrip(CRUDBase[models.Trip, schemas.TripCreate, schemas.TripUpdate]):
    def get_multi_by_owner(
        self, db: Session, *, skip: int = 0, limit: int | None = None, user_id: str
    ) -> list[models.Trip]:
        trips = (
            db.query(self._model)
            .filter_by(user_id=user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return trips


trip = CRUDTrip(models.Trip)
