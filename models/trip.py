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
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db.base_class import Base
from schemas import TripType


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

    user = relationship("User", back_populates="trips")
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
