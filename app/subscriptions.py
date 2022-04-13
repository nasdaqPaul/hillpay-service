from mongoengine.errors import DoesNotExist, ValidationError

from app.db.documents.member import MemberDocument, SubscriptionDocument
from app.db.documents.service import ServiceDocument


def new_subscription(member_id: str, service_id):
    try:
        service = ServiceDocument.objects.get(id=service_id)
    except (DoesNotExist, ValidationError):
        raise Exception("ServiceNotFound")
    try:
        new_sub = SubscriptionDocument(service=service)
        member = MemberDocument.objects.get(id=member_id)
        for subscription in member.subscriptions:
            if subscription.service.id == new_sub.service.id:
                return
        member.subscriptions.append(new_sub)
        member.save()
        return new_sub
    except DoesNotExist:
        print('doesnt exist')


def unsubscribe_from_service(member_id: str, service_id: str):
    try:
        service = ServiceDocument.objects.get(id=service_id)
    except (DoesNotExist, ValidationError):
        raise Exception("ServiceNotFound")
    member = MemberDocument.objects.get(id=member_id)
    member.subscriptions = [active_sub for active_sub in member.subscriptions if str(active_sub.service.id) != service_id]
    member.save()
