from typing import List

from bson.objectid import ObjectId

from app.db.documents.member import MemberDocument, Bill
from app.db.documents.payment_request import PaymentRequestDocument
from app.exceptions import BillInPaymentRequestException


def sublist(lst1, lst2):
    """
    Checks if lst1 is sublist of lst2
    :param lst1:
    :param lst2:
    :return:
    """
    if set(lst1) == set(lst2):
        return True
    ls1 = [element for element in lst1 if element in lst2]
    ls2 = [element for element in lst2 if element in lst1]

    print('lst1', ls1)
    print('lst2', ls2)

    return set(ls1) == set(ls2)


def calculate_bill_request_amount(bills: List[Bill]):
    total_amount = 0
    for bill in bills:
        total_amount += bill.amount
    return total_amount


def save_payment_request(member: MemberDocument, requested_bill_ids: List[str]):
    requested_bill_ids = list(set(requested_bill_ids))
    member_bill_ids = [str(bill._id) for bill in member.bills]

    if not sublist(requested_bill_ids, member_bill_ids):
        raise Exception('Bills not in member bills')
    pending_payment_requests = PaymentRequestDocument.objects(member=member)

    if pending_payment_requests:
        already_requested = []
        for pending_payment_request in pending_payment_requests:
            already_requested.extend(
                [bill_id for bill_id in pending_payment_request.bills if str(bill_id) in requested_bill_ids])
        if already_requested:
            raise BillInPaymentRequestException()

    new_payment_request = PaymentRequestDocument(
        member=member,
        bills=[ObjectId(item) for item in requested_bill_ids],
        amount=calculate_bill_request_amount(
            [bill for bill in member.bills if bill.id in requested_bill_ids]
        )
    )
    new_payment_request.save()
    return new_payment_request
