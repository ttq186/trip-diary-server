from schemas import CamelModel


class TripLikeBase(CamelModel):
    id: int | None = None
    trip_id: int | None = None
    user_id: str | None = None


class TripLikeCreate(TripLikeBase):
    pass


class TripLikeUpdate(TripLikeBase):
    pass


class TripLikeOut(TripLikeBase):
    pass

    class Config:
        orm_mode = True
