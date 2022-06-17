from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db.base_class import Base
from schemas import FileType


class LocationFile(Base):
    __tablename__ = "location_file"

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    type = Column(Enum(FileType), default=FileType.IMAGE)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    location_id = Column(Integer, ForeignKey("location.id", ondelete="CASCADE"))

    location = relationship("Location", back_populates="files")
