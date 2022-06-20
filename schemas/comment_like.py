from schemas import CamelModel


class CommentLikeBase(CamelModel):
    id: int | None = None
    comment_id: int | None = None
    user_id: str | None = None


class CommentLikeCreate(CommentLikeBase):
    pass


class CommentLikeUpdate(CommentLikeBase):
    pass


class CommentLikeOut(CommentLikeBase):
    class Config:
        orm_mode = True
