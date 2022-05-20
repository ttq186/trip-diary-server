from sqlalchemy import Column, Text, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db.base_class import Base


class TripComment(Base):
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(DateTime(timezone=True))
    trip_id = Column(Integer, ForeignKey("trip.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populated="trip_comments")
    trip = relationship("Trip", back_populated="trip_comments")
