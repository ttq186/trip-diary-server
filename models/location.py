from sqlalchemy import Column, ForeignKey, String, Text, Integer, Float, Date
from sqlalchemy.orm import relationship

from db.base_class import Base


class Location(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True)
    review = Column(Text, nullable=False)
    lat = Column(Float)
    lng = Column(Float)
    start_at = Column(Date)
    trip_id = Column(Integer, ForeignKey("trip.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    trip = relationship("Trip", back_populates="locations")
    location_images = relationship("LocationImage", back_populates="location")
