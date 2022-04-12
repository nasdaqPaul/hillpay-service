from typing import Optional

from pydantic import BaseModel, Field, EmailStr

from app.api.models import BaseResponseModel
from app.db.documents.member import Role, AccountStatus


class AccountModel(BaseModel):
    role: Role = Field(Role.MEMBER)
    status: AccountStatus = Field(AccountStatus.INACTIVE)

    class Config:
        orm_mode = True


class MemberModel(BaseModel):
    first_name: Optional[str] = Field(None, alias='firstName')
    last_name: Optional[str] = Field(None, alias='lastName')
    email: Optional[EmailStr] = Field(None)
    phone: Optional[str] = Field(None)
    account: AccountModel


class MemberResponseModel(BaseResponseModel, MemberModel):
    id: str
    first_name: Optional[str] = Field(None, alias='firstName')
    last_name: Optional[str] = Field(None, alias='lastName')


class AccountSetupModel(BaseModel):
    password: str = Field(...)


class MemberSetupModel(MemberModel):
    account: AccountSetupModel
