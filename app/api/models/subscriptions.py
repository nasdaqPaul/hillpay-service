from pydantic import BaseModel, Field


class SubscriptionRequestModel(BaseModel):
    service_id: str = Field(..., alias='serviceId')
