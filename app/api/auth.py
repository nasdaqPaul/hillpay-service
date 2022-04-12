from datetime import timedelta, datetime
from typing import Optional, List, Callable

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError

from app.api.exceptions import AuthenticationException, AuthorizationException
from app.api.models import MemberResponseModel
from app.api.models.member import MemberModel
from app.db.documents.member import Role, MemberDocument

oauth_scheme = OAuth2PasswordBearer(tokenUrl='sessions')

# TODO: Put these in an environment variable
SECRET_KEY = 'some random string'
JWT_ALGORITHM = 'HS256'


def decode_jwt(access_token: str):
    return jwt.decode(access_token, SECRET_KEY, algorithms=[JWT_ALGORITHM])


def refresh_token(access_token: str):
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except ExpiredSignatureError:
        payload = jwt.get_unverified_claims(access_token)
    return generate_access_token(payload)


def generate_access_token(payload: dict, expires: Optional[timedelta] = None) -> dict:
    """
    Creates an JWT access token with the speficied payload

    :param payload: Data to encode in the JWT
    :param expires: Duration of the token
    :return: Access Token
    """
    data = payload.copy()
    if expires:
        exp = datetime.utcnow() + expires
    else:
        exp = datetime.utcnow() + timedelta(minutes=60)
    data.update({
        'exp': exp
    })
    return {
        "access_token": jwt.encode(data, SECRET_KEY, algorithm=JWT_ALGORITHM),
        "token_type": 'bearer'
    }


def get_authenticated_member(access_token: str = Depends(oauth_scheme)) -> MemberModel:
    """
    Decoded a JWT from the request header and returns a dict representing the authenticated user

    :return: MemberModel: Model of the authenticated user
    """
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except JWTError:
        raise AuthenticationException()
    return MemberResponseModel(**payload)


def get_authenticated_member_as_doc(access_token: str = Depends(oauth_scheme)) -> MemberDocument:
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except JWTError:
        raise AuthenticationException()
    return MemberDocument.objects.get(id=payload['id'])


def get_authorized_member(roles: List[Role]) -> Callable[[MemberResponseModel], MemberResponseModel]:
    """
    Provides primitive role-based authorization

    :param roles: A list or permitted roles
    :return: A dependency
    """

    def callback(authenticated_member: MemberResponseModel = Depends(get_authenticated_member)):
        if authenticated_member.dict()['role'] not in roles:
            raise AuthorizationException()
        return authenticated_member

    return callback
