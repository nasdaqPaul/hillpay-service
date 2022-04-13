from datetime import datetime

from pydantic import BaseModel, Field

from app.api.models import BaseResponseModel


class SubscriptionRequestModel(BaseModel):
    service_id: str = Field(..., alias='serviceId')


class SubscriptionResponseModel(BaseResponseModel):
    service_id: str = Field(..., alias='serviceId')
    subscription_date: datetime  = Field(..., alias='subscriptionDate')
