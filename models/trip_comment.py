from sqlalchemy import Column, Text, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db.base_class import Base


class TripComment(Base):
    __tablename__ = "trip_comment"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(DateTime(timezone=True))
    comment_id = Column(Integer, ForeignKey("trip_comment.id", ondelete="CASCADE"))
    trip_id = Column(Integer, ForeignKey("trip.id", ondelete="CASCADE"))
    user_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="trip_comments")
    trip = relationship("Trip", back_populates="comments")
    comments = relationship("TripComment")
