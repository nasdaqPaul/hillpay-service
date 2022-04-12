from typing import List

from fastapi import APIRouter, Depends

from app.api.auth import get_authenticated_member
from app.api.models import MemberResponseModel
from app.api.models.services import CourtServiceRequestModel, CourtServiceResponseModel
from app.api.models.subscriptions import SubscriptionRequestModel
from app.service import create_service, get_all_services as get_all_court_services
from app.subscriptions import subscribe_to_service as sub, get_all_subscriptions as get_all_subs, \
    unsubscribe_from_service as unsub

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
    """
    Return a list of services that I am elligable for
    :return:
    """
    return get_all_court_services()


@services_router.get('/me/subscriptions')
def get_all_subscriptions(member: MemberResponseModel = Depends(get_authenticated_member)):
    """

    :return:
    """

    return get_all_subs(member.id)


@services_router.post('/me/subscriptions')
def subscribe_to_service(service: SubscriptionRequestModel,
                         member: MemberResponseModel = Depends(get_authenticated_member)):
    """
    Subscribe to a service
    """
    sub(member.id, service.service_id)


@services_router.delete('/me/subscription/{service_id}')
def unsubscribe_from_service(service_id: str, member: MemberResponseModel = Depends(get_authenticated_member)):
    """
    Unsubs a member from a service
    """
    unsub(member.id, service_id)
