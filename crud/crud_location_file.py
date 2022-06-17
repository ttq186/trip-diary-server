from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models import LocationFile
from schemas import LocationFileCreate, LocationFileUpdate


class CRUDLocationImage(CRUDBase[LocationFile, LocationFileCreate, LocationFileUpdate]):
    def get_multi_by_location_id(
        self, db: Session, location_id: int, skip: int = 0, limit: int | None = None
    ) -> list[LocationFile]:
        location_files = (
            db.query(LocationFile)
            .filter_by(location_id=location_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return location_files


location_file = CRUDLocationImage(LocationFile)
