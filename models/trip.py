from sqlalchemy import Column, String, Integer, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from db.base_class import Base


class Trip(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    cover_img_url = Column(String)
    from_coordinates = Column(Geometry(geometry_type="POINT", srid=4326))
    to_coordinates = Column(Geometry(geometry_type="POINT", srid=4326))
    day_count = Column(Integer, default=1)
    departure_at = Column(DateTime(timezone=True))
    back_trip_at = Column(DateTime(timezone=True))
    is_public = Column(Boolean, default=True)

    user = relationship("User", back_populated="trips")
    comments = relationship("TripComment", back_populated="trip")
    likes = relationship("TripLike", back_populated="trip")
    checklist_items = relationship("ChecklistItem", back_populated="trip")
    locations = relationship("Location", back_populated="trip")
