from pydantic import BaseModel


class BaseResponseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        orm_mode = True


# Imports not on top of file to prevent circular dependency
from .member import MemberResponseModel, MemberModel
from .session import SessionResponseModel
