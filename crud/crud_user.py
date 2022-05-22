from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models import User
from schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, email: str):
        user = db.query(User).filter_by(email=email).first()
        return user


user = CRUDUser(User)
