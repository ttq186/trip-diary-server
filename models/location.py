from sqlalchemy import Column, ForeignKey, String, Text, Integer, Float, Date
from sqlalchemy.orm import relationship

from db.base_class import Base


class Location(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True)
    review = Column(Text)
    lat = Column(Float)
    lng = Column(Float)
    start_at = Column(Date)
    trip_id = Column(Integer, ForeignKey("trip.id", ondelete="CASCADE"))
    user_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"))

    trip = relationship("Trip", back_populates="locations")
    images = relationship("LocationImage", back_populates="location")
