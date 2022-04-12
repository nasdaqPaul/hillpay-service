from typing import Optional, List

from app.db.documents.member import MemberTypeEnum
from app.db.documents.service import ServiceDocument, ServiceBillingDocument


class Service:
    pass


def create_service(name: str, billing: dict, eligibility: List[MemberTypeEnum], status: Optional[str], model: str,
                   description: Optional[str] = None):
    """
    Creates a new service
    :
    :return:
    """
    service_document = ServiceDocument(name=name, status=status, description=description, eligibility=eligibility)
    billing_document = ServiceBillingDocument(amount=billing['amount'], interval=billing['interval'])

    service_document.billing = billing_document
    service_document.save()


def get_all_services():
    """
    Returns all services
    :return:
    """
    all_services = ServiceDocument.objects()
    serialized_services = []
    for service in all_services:
        s = service.to_mongo().to_dict()
        s['id'] = str(s.pop('_id'))
        serialized_services.append(s)
    return serialized_services
