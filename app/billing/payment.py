from app.db.documents.member import MemberDocument
from app.db.documents.payment_request import PaymentRequestDocument


def make_payment(payment_request: PaymentRequestDocument):
    member = MemberDocument.objects.get(id=payment_request.member.id)
