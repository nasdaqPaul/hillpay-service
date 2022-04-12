from fastapi import HTTPException


class AuthenticationException(HTTPException):
    """
    Exception raised when request header contains invalid token
    """

    def __init__(self):
        super().__init__(status_code=401, detail='Authentication Required')


class InvalidCredentialsException(HTTPException):
    """
    Exception raised when email/phone number provided are invalid
    """

    def __init__(self):
        super().__init__(status_code=401, detail='Authentication Required')


class AuthorizationException(HTTPException):
    """
    Exception raised when endpoint is not permitted by authenticated member
    """

    def __init__(self):
        super().__init__(status_code=403, detail='Not authorized')


class MemberNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail='Member not found')


class BillInPaymentRequest(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail='A payment request already exists with bill item(s)')
