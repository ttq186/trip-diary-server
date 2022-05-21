from sqlalchemy import Column, ForeignKey, String, Integer, Float
from sqlalchemy.orm import relationship

from db.base_class import Base


class Location(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True)
    reivew = Column(String, nullable=False)
    lat = Column(Float)
    lng = Column(Float)
    trip_id = Column(Integer, ForeignKey("trip.id", ondelete="CASCADE"), nullable=False)

    trip = relationship("Trip", back_populates="locations")
    location_images = relationship("LocationImage", back_populates="location")
