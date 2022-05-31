from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models import ChecklistItem
from schemas import CheckListItemCreate, CheckListItemUpdate


class CRUDChecklistItem(
    CRUDBase[ChecklistItem, CheckListItemCreate, CheckListItemUpdate]
):
    def get_multi_by_trip_id(
        self, db: Session, trip_id: int, skip: int = 0, limit: int | None = None
    ) -> list[ChecklistItem]:
        checklist = (
            db.query(ChecklistItem)
            .filter_by(trip_id=trip_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return checklist


checklist_item = CRUDChecklistItem(ChecklistItem)
