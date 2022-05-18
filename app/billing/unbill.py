from bson import ObjectId

from app.db.documents.member import MemberDocument
from app.db.documents.payment_request import PaymentRequestDocument


def unbill(payment_request: PaymentRequestDocument):
    member: MemberDocument = payment_request.member.fetch()
    new_bills = [bill for bill in member.bills if ObjectId(bill.id) not in payment_request.bills]

    print(new_bills)
    member.bills = new_bills
    payment_request.delete()
    member.save()
    # print(payment_request.member.fetch().first_name)
