from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm

from app.api.auth import generate_access_token, refresh_token
from app.api.models import SessionResponseModel, MemberResponseModel
from app.auth import authenticate_member

session_routes = APIRouter(tags=['auth'])


@session_routes.post('/sessions', response_model=SessionResponseModel)
def create_session(login_credentials: OAuth2PasswordRequestForm = Depends()):
    """
    Creates a login session for a member
    """
    user = authenticate_member(login_credentials.username, login_credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email, phone number or password")
    return generate_access_token(MemberResponseModel.from_orm(user).dict(exclude_none=True, by_alias=True))


@session_routes.put('/sessions', response_model=SessionResponseModel)
def refresh_access_token(authorization: str = Header(...)):
    token = authorization.split(' ')[1]
    return refresh_token(token)


@session_routes.delete('/sessions')
def log_out():
    """
    Invalidates an access token, essentially logging the user out
    """
    pass
