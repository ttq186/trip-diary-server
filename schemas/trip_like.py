from schemas import CamelModel


class TripLikeBase(CamelModel):
    trip_id: int | None = None
    user_id: str | None = None


class TripLikeCreate(TripLikeBase):
    pass


class TripLikeUpdate(TripLikeBase):
    pass


class TripLikeInDbBase(TripLikeBase):
    class Config:
        orm_mode = True


class TripLikeInDb(TripLikeBase):
    pass


class TripLikeOut(TripLikeInDb):
    pass
