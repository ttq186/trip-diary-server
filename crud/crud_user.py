from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models import User
from schemas import UserCreate, UserUpdate
from core.security import get_hashed_password


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, email: str) -> User | None:
        # user = db.query(self._model).filter_by(email=email).first()
        user = db.query(User).filter_by(email=email).first()
        return user

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        new_user_data = obj_in.dict()
        new_user_data["password"] = get_hashed_password(new_user_data["password"])
        db_obj = User(**new_user_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


user = CRUDUser(User)
