from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Integer,
    Text,
    Date,
    Boolean,
    Float,
)
from sqlalchemy.orm import relationship

from db.base_class import Base


class Trip(Base):
    __tablename__ = "trip"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    cover_img_url = Column(String)
    from_lat = Column(Float, nullable=False)
    from_lng = Column(Float, nullable=False)
    to_lat = Column(Float, nullable=False)
    to_lng = Column(Float, nullable=False)
    start_at = Column(Date, nullable=False)
    finish_at = Column(Date)
    back_trip_at = Column(Date)
    is_public = Column(Boolean, default=True)
    user_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="trips")
    comments = relationship("TripComment", back_populates="trip")
    likes = relationship("TripLike", back_populates="trip")
    checklist_items = relationship("ChecklistItem", back_populates="trip")
    locations = relationship("Location", back_populates="trip")
