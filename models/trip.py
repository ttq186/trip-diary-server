from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Integer,
    Text,
    DateTime,
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
    from_lat = Column(Float)
    from_lng = Column(Float)
    to_lat = Column(Float)
    to_lng = Column(Float)
    day_count = Column(Integer)
    departure_at = Column(DateTime(timezone=True))
    back_trip_at = Column(DateTime(timezone=True))
    is_public = Column(Boolean, default=True)
    user_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="trips")
    comments = relationship("TripComment", back_populates="trip")
    likes = relationship("TripLike", back_populates="trip")
    checklist_items = relationship("ChecklistItem", back_populates="trip")
    locations = relationship("Location", back_populates="trip")
