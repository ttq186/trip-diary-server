from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Integer,
    Text,
    Date,
    DateTime,
    Boolean,
    Float,
    Enum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property

from db.base_class import Base
from schemas import TripType
from schemas.trip import TripScope
from .user import User


class Trip(Base):
    __tablename__ = "trip"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    cover_img_url = Column(String)
    from_lat = Column(Float, nullable=False)
    to_lat = Column(Float, nullable=False)
    from_lng = Column(Float, nullable=False)
    to_lng = Column(Float, nullable=False)
    start_at = Column(Date, nullable=False)
    back_trip_at = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_finished = Column(Boolean, default=False)
    is_public = Column(Boolean, default=True)
    can_be_reminded = Column(Boolean, default=True)
    user_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"))
    scope = Column(Enum(TripScope))

    author = relationship("User", back_populates="trips")
    comments = relationship("TripComment", back_populates="trip")
    likes = relationship("TripLike", back_populates="trip")
    checklist_items = relationship("ChecklistItem", back_populates="trip")
    locations = relationship("Location", back_populates="trip")

    @property
    def num_of_likes(self) -> int:
        if self.likes is None:
            return 0
        return len(self.likes)

    @property
    def type(self) -> TripType:
        if self.back_trip_at is None:
            return TripType.SINGLE
        return TripType.AROUND

    @hybrid_property
    def author_username(self) -> str:
        pass

    @author_username.expression
    def author_username(cls) -> str:
        return User.username

    @hybrid_property
    def author_first_name(self) -> str:
        pass

    @author_first_name.expression
    def author_first_name(cls):
        return User.first_name

    @hybrid_property
    def author_last_name(self) -> str:
        pass

    @author_last_name.expression
    def author_last_name(cls):
        return User.last_name

    @hybrid_property
    def author_email(self) -> str:
        pass

    @author_email.expression
    def author_email(cls) -> str:
        return User.email
