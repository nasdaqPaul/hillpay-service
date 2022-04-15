from datetime import date
from typing import Optional

from pydantic import Field

from app.api.models import BaseResponseModel


class BillResponseModel(BaseResponseModel):
    id: str
    service_id: str = Field(..., alias='serviceId')
    amount: int

    day: Optional[date] = Field(None)
    month: Optional[date] = Field(None)
