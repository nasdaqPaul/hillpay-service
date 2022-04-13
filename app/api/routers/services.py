from typing import List, Optional

from fastapi import APIRouter, Depends

from app.api.auth import get_authenticated_member, get_authenticated_member_as_doc
from app.api.models import MemberResponseModel
from app.api.models.services import CourtServiceRequestModel, CourtServiceResponseModel
from app.api.models.subscriptions import SubscriptionRequestModel, SubscriptionResponseModel
from app.db.documents.member import MemberDocument
from app.service import create_service, get_all_services as get_all_court_services
from app.subscriptions import unsubscribe_from_service as unsub, new_subscription

services_router = APIRouter()


@services_router.post('/court/services')
def add_service(service: CourtServiceRequestModel):
    create_service(**service.dict(exclude_none=True))
    return


@services_router.get("/court/services", response_model=List[CourtServiceResponseModel])
async def get_all_services():
    """
    Returns all services in the court

    :return:
    """
    return get_all_court_services()


@services_router.get('/me/services', response_model=List[CourtServiceResponseModel])
def get_services():
    return get_all_court_services()


@services_router.get('/me/subscriptions', response_model=List[SubscriptionResponseModel])
def get_all_subscriptions(member: MemberDocument = Depends(get_authenticated_member_as_doc)):
    return member.subscriptions


@services_router.post('/me/subscriptions', response_model=Optional[SubscriptionResponseModel])
def subscribe_to_service(service: SubscriptionRequestModel,
                         member: MemberResponseModel = Depends(get_authenticated_member)):
    new_sub = new_subscription(member.id, service.service_id)
    return new_sub


@services_router.delete('/me/subscription/{service_id}')
def unsubscribe_from_service(service_id: str, member: MemberResponseModel = Depends(get_authenticated_member)):
    unsub(member.id, service_id)
