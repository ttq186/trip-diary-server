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


class InvalidEmail(HTTPException):
    def __init__(self):
        detail = "This email is invalid!"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class IncorrectLoginCredentials(HTTPException):
    def __init__(self):
        detail = "Incorrect email or password. Try again!"
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class AccountCreatedWithOutGoogle(HTTPException):
    def __init__(self):
        detail = (
            "Looks like an account has been created before without "
            "Google sign in method. Try again!"
        )
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class AccountCreatedByGoogle(HTTPException):
    def __init__(self):
        detail = (
            "Looks like this account has been created by "
            "Google sign in method. Try again!"
        )
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class EmailNotExists(HTTPException):
    def __init__(self):
        detail = "This email does not exist. Try again!"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ResetLinkExpired(HTTPException):
    def __init__(self):
        detail = "This reset link has expired. Try again!"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class LikeAlreadyMade(HTTPException):
    def __init__(self, resource_type: str) -> None:
        detail = f"You already liked this {resource_type.lower()}!"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class LikeHasNotBeenMade(HTTPException):
    def __init__(self, resource_type: str) -> None:
        detail = f"You haven't liked this {resource_type.lower()}!"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class TripCommentHasNotBeenMade(HTTPException):
    def __init__(self) -> None:
        detail = "You haven't commented on this trip!"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class TripCantBeReminded(HTTPException):
    def __init__(self) -> None:
        detail = "This trip can't be reminded anymore!"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
