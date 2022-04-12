from typing import List

from pydantic import Field

from app.api.models import BaseResponseModel


class PaymentRequestResponseModel(BaseResponseModel):
    id: str
    member_id: str = Field(..., alias='memberId')
    bills: List[str]
    amount: int