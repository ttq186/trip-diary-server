from curses.ascii import HT
from fastapi import status, HTTPException


class NotAuthorized(HTTPException):
    def __init__(self) -> None:
        detail = "You don't have this privilege!"
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class ResourceNotFound(HTTPException):
    def __init__(self, resource_type, id) -> None:
        detail = f"{resource_type} with id {id} not found!"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class EmailAlreadyExists(HTTPException):
    def __init__(self):
        detail = "Email already exist!"
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)
