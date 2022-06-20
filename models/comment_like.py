from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

from db.base_class import Base


class CommentLike(Base):
    __tablename__ = "comment_like"

    id = Column(Integer, primary_key=True)
    comment_id = Column(Integer, ForeignKey("trip_comment.id", ondelete="CASCADE"))
    user_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="comment_likes")
    comment = relationship("TripComment", back_populates="likes")
