from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models import LocationImage
from schemas import LocationImageCreate, LocationImageUpdate


class CRUDLocationImage(
    CRUDBase[LocationImage, LocationImageCreate, LocationImageUpdate]
):
    def get_multi_by_location_id(
        self, db: Session, location_id: int, skip: int = 0, limit: int | None = None
    ) -> list[LocationImage]:
        location_images = (
            db.query(LocationImage)
            .filter_by(location_id=location_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return location_images


location_image = CRUDLocationImage(LocationImage)
