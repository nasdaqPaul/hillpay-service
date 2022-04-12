from typing import Optional

from pydantic import BaseModel, Field
from pydantic.class_validators import List

from app.db.documents.member import MemberTypeEnum
from app.db.documents.service import BillingIntervalEnum, ServiceStatusEnum, ServiceModelEnum


class BillingModel(BaseModel):
    amount: int = Field(..., gt=0)
    interval: Optional[BillingIntervalEnum] = Field(None)


class CourtServiceRequestModel(BaseModel):
    name: str = Field(...)
    description: Optional[str] = Field(None)
    billing: BillingModel
    model: ServiceModelEnum = ServiceModelEnum.RENEWABLE
    status: ServiceStatusEnum = Field(ServiceStatusEnum.ACTIVE)
    eligibility: List[MemberTypeEnum] = Field([MemberTypeEnum.TENANT, MemberTypeEnum.PERMANENT])


class CourtServiceResponseModel(CourtServiceRequestModel):
    id: str = Field(...)
