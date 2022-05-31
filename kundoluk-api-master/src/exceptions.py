from fastapi import HTTPException


class UnsuccessfulAuthenticationError(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=401,
            detail='Wrong credentials or authentication error.',
        )


class CookiesExpiredOrDoNotExistError(UnsuccessfulAuthenticationError):
    pass
