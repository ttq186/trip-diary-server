from schemas import CamelModel


class TokenOut(CamelModel):
    """Properties to return to client."""

    access_token: str
    token_type: str


class TokenIn(CamelModel):
    id: str | None = None


class GoogleToken(CamelModel):
    token_id: str
