from sqlalchemy import Column, DateTime, Date, String, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.base_class import Base
import utils


class User(Base):
    __tablename__ = "user"
    id = Column(String, primary_key=True, default=utils.generate_uuid())
    email = Column(String, nullable=False)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    avatar_url = Column(String)
    cover_img_url = Column(String)
    is_female = Column(Boolean)
    description = Column(Text)
    country = Column(String)
    date_of_birth = Column(Date)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    is_admin = Column(Boolean, default=False)

    trips = relationship("Trip", back_populates="author")
    trip_comments = relationship("TripComment", back_populates="user")
    trip_likes = relationship("TripLike", back_populates="user")

    @property
    def fullname(self) -> str:
        return self.first_name + self.last_name

    @property
    def num_of_trips(self) -> int:
        if self.trips is None:
            return 0
        return len(self.trips)
