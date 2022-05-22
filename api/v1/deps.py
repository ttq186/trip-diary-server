from typing import Generator

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt, ExpiredSignatureError

import models
import schemas
import exceptions
from core.config import settings
from db.session import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, key=settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM
        )
        id = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenIn(id=id)
        user = db.query(models.User).filter_by(id=token_data.id).first()

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired!"
        )
    except JWTError:
        raise credentials_exception
    if user is None:
        raise credentials_exception
    return


def get_current_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_admin:
        raise exceptions.NotAuthorized()
    return current_user
