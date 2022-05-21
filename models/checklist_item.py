from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base


class ChecklistItem(Base):
    __tablename__ = "checklist_item"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    notes = Column(Text)
    has_prepared = Column(Boolean, default=False)
    trip_id = Column(Integer, ForeignKey("trip.id", ondelete="CASCADE"), nullable=False)

    trip = relationship("Trip", back_populates="checklist_items")
