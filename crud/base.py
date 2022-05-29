from typing import TypeVar, Generic, Dict, Any

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from db.base import Base
from schemas import CamelModel

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=CamelModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=CamelModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: ModelType):
        """
        CRUD Object with default methods to Create, Read, Update, Delete.

        **Parameter**

        * `model`: A SQLAlchemy model
        * `schema`: A Pydantic model
        """
        self._model = model

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self._model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: str) -> ModelType | None:
        return db.query(self._model).filter_by(id=id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int | None = None
    ) -> list[ModelType]:
        return db.query(self._model).offset(skip).limit(limit).all()

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | Dict[str, Any]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(db_obj, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: str) -> ModelType | None:
        deleted_obj = self.get(db, id)
        db.delete(deleted_obj)
        db.commit()
        return deleted_obj
