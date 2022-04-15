from pydantic.datetime_parse import date

from app.db.documents.member import MemberDocument, Bill, SubscriptionDocument
from app.db.documents.service import BillingIntervalEnum, ServiceDocument


def calculate_bill_amount(subscription: SubscriptionDocument, service: ServiceDocument):
    return service.billing.amount


def bill_this_month():
    all_members = MemberDocument.objects
    for member in all_members:  # type: MemberDocument
        for subscription in member.subscriptions:  # type: SubscriptionDocument
            service = subscription.service.fetch()
            if service.billing.interval == BillingIntervalEnum.MONTHLY:
                billed = False
                today = date.today()

                if member.bills:
                    for bill in member.bills:  # type: Bill
                        if bill.month == today and bill.service.id == subscription.service.id:
                            billed = True
                if billed:
                    continue
                new_bill = Bill(service=subscription.service,
                                amount=calculate_bill_amount(subscription, service), month=today)
                member.bills.append(new_bill)
                member.save()

bill_this_month()