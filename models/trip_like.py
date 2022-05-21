from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

from db.base_class import Base


class TripLike(Base):
    __tablename__ = "trip_like"

    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey("trip.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="trip_likes")
    trip = relationship("Trip", back_populates="trip_likes")
