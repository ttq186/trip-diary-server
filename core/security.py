from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"])


def create_access_token(
    encoded_data: dict,
    expires_delta: Optional[timedelta] = None,
    jwt_secret_key: str | None = settings.JWT_SECRET_KEY,
) -> str | None:
    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    encoded_data.update({"exp": expire})
    try:
        jwt_token = jwt.encode(
            encoded_data, jwt_secret_key, algorithm=settings.JWT_ALGORITHM
        )
        return jwt_token
    except JWTError:
        return None


def decode_jwt_token(
    token: str,
    key: str | None = settings.JWT_SECRET_KEY,
    algorithm: str | None = settings.JWT_ALGORITHM,
) -> dict | None:
    try:
        token_data = jwt.decode(token, key, algorithm)
        return token_data
    except Exception:
        return None


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_pwd: str, hashed_pwd: str) -> bool:
    return pwd_context.verify(plain_pwd, hashed_pwd)
