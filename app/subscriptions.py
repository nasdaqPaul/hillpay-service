from mongoengine.errors import DoesNotExist, ValidationError

from app.db.documents.member import MemberDocument, SubscriptionDocument
from app.db.documents.service import ServiceDocument


def subscribe_to_service(member_id: str, service_id) -> None:
    try:
        service = ServiceDocument.objects.get(id=service_id)
    except (DoesNotExist, ValidationError):
        raise Exception("ServiceNotFound")
    try:
        new_subscription = SubscriptionDocument(service=service)
        member = MemberDocument.objects.get(id=member_id)
        for subscription in member.subscriptions:
            if subscription.service.id == new_subscription.service.id:
                return
        member.subscriptions.append(new_subscription)
        member.save()
    except DoesNotExist:
        print('doesnt exist')


def get_all_subscriptions(member_id: str):
    """
    Ruturns all the subs of a member

    :return:
    """
    try:
        member = MemberDocument.objects.get(id=member_id)
        return [str(sub.id) for sub in member.subscriptions]
    except DoesNotExist:
        raise Exception('MemberNotFound')


def unsubscribe_from_service(member_id: str, service_id: str):
    """
    Unsubs a member from a service
    :param member_id:
    :param service_id:
    :return:
    """
    try:
        service = ServiceDocument.objects.get(id=service_id)
    except (DoesNotExist, ValidationError):
        raise Exception("ServiceNotFound")
    try:
        MemberDocument.objects.get(id=member_id).update(pull__subscriptions=service)
    except Exception as e:
        print(e)
        raise Exception('SomeError')
