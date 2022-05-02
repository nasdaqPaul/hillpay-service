from datetime import date

from app.db.documents.member import Bill
from app.db.documents.member import MemberDocument
from app.db.documents.member import SubscriptionDocument
from app.db.documents.service import ServiceDocument, BillingIntervalEnum


def filter_members_by_daily_subscriptions(member: MemberDocument):
    for subscription in member.subscriptions:  # type: SubscriptionDocument
        service: ServiceDocument = subscription.service.fetch()
        if service.billing.interval == BillingIntervalEnum.DAILY:
            return True
        else:
            return False


def filter_subscriptions_by_model_daily(subscription: SubscriptionDocument):
    service = subscription.service.fetch()
    if service.billing.interval == BillingIntervalEnum.DAILY:
        return True
    else:
        return False


def calculate_bill_amount(subscription: SubscriptionDocument, service: ServiceDocument):
    today = date.today()
    if subscription.subscription_date == today:
        return service.billing.amount / 2
    return service.billing.amount


def bill_daily():
    all_members = MemberDocument.objects
    for member in all_members:  # type: MemberDocument
        for subscription in member.subscriptions:  # type: SubscriptionDocument
            service = subscription.service.fetch()
            if service.billing.interval == BillingIntervalEnum.DAILY:
                billed = False
                today = date.today()
                if member.bills:
                    for bill in member.bills:  # type: Bill
                        if bill.day:
                            if bill.day.day == today.day and bill.service.id == subscription.service.id:
                                billed = True
                if billed:
                    continue
                new_bill = Bill(service=subscription.service,
                                amount=calculate_bill_amount(subscription, service), day=today)
                member.bills.append(new_bill)
                member.save()
    # member_with_daily_subs = filter(filter_members_by_daily_subscriptions, all_members)
    # del all_members
    #
    # for member in member_with_daily_subs:
    #     daily_subscriptions = filter(filter_subscriptions_by_model_daily, member.subscriptions)
    #     for daily_subscription in daily_subscriptions:
    #         bill_member(member, daily_subscription)


def bill_member(member: MemberDocument, subscription: SubscriptionDocument):
    today = date.today()
    if member.bills:
        for bill in member.bills:  # type: Bill
            if bill.day == today and bill.service.id == subscription.service.id:
                print('billed')
                return
    new_bill = Bill(service=subscription.service, amount=200, day=today)
    member.bills.append(new_bill)
    member.save()


bill_daily()
