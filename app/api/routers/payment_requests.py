from fastapi import APIRouter, Depends, Request
from pydantic.class_validators import List

from app.api.auth import get_authenticated_member, get_authenticated_member_as_doc
from app.api.exceptions import BillInPaymentRequest as BillInPaymentRequestHTTPException
from app.api.models import MemberResponseModel
from app.api.models.payment_request import PaymentRequestResponseModel
from app.api.ws import manager
from app.daraja.auth import verify_request_signature
from app.daraja.daraja_requests import queue_stk_request
from app.db.documents.member import MemberDocument
from app.db.documents.payment_request import PaymentRequestDocument
from app.exceptions import BillInPaymentRequestException
from app.payments import save_payment_request

payment_requests_router = APIRouter()


@payment_requests_router.get('/me/payment-requests', response_model=List[PaymentRequestResponseModel])
def get_payment_requests(member: MemberResponseModel = Depends(get_authenticated_member)):
    all_payment_requests = list(PaymentRequestDocument.objects(member=MemberDocument.objects.get(id=member.id)))
    for payment_request in all_payment_requests:  # type: PaymentRequestDocument
        payment_request.id = str(payment_request.id)
        payment_request.bills = [str(bill) for bill in payment_request.bills]

    return all_payment_requests


@payment_requests_router.post('/payment-requests', response_model=PaymentRequestResponseModel, status_code=201)
def request_payment(bill_items: List[str], member: MemberDocument = Depends(get_authenticated_member_as_doc)):
    try:
        payment_request = save_payment_request(member, bill_items)
    except BillInPaymentRequestException:
        raise BillInPaymentRequestHTTPException()
    payment_request.id = str(payment_request.id)
    payment_request.bills = [str(bill) for bill in payment_request.bills]

    print(f"{member.first_name} {member.last_name}")
    queue_status = queue_stk_request(
        254743421389,
        payment_request.amount,
        member.mpesa.get_account_number(),
        {'id': payment_request.id, 'memberId': str(member.id)},
        "payment-request-results"
    )
    print(queue_status)
    return payment_request


@payment_requests_router.post('/payment-request-results/{signature}')
async def confirm_payment(signature: str, request: Request):
    req_body = await request.json()
    print(req_body)
    signed_payload = verify_request_signature(signature)
    payment_request = PaymentRequestDocument.objects.get(id=signed_payload['id'])
    payment_request.delete()
    await manager.send_json(signed_payload['memberId'], req_body)
