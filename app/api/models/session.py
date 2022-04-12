from pydantic import Field

from app.api.models import BaseResponseModel


class SessionResponseModel(BaseResponseModel):
    access_token: str = Field(..., description='JWT Access Token')
    token_type: str = Field(...)
