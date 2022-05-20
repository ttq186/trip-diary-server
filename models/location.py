from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from db.base_class import Base


class Location(Base):
    id = Column(Integer, primary_key=True)
    reivew = Column(String, nullable=False)
    coordinates = Column(Geometry(geometry_type="POINT", srid=4326))
    trip_id = Column(Integer, ForeignKey("trip.id", ondelete="CASCADE"), nullable=False)

    trip = relationship("Trip", back_populated="locations")
    location_images = relationship("LocationImage", back_populated="location")
