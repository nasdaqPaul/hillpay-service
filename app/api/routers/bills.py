from typing import List

from fastapi import APIRouter, Depends

from app.api.auth import get_authenticated_member
from app.api.models import MemberResponseModel
from app.api.models.bill import BillResponseModel
from app.db.documents.member import MemberDocument

bills_router = APIRouter()


@bills_router.get('/me/bills', response_model=List[BillResponseModel])
def get_all_bills(member: MemberResponseModel = Depends(get_authenticated_member)):
    member_document: MemberDocument = MemberDocument.objects.get(id=member.id)
    return member_document.bills


@bills_router.delete('/me/bills')
def settle_bills(ids: List[str], member: MemberResponseModel = Depends(get_authenticated_member)):
    print(ids)
    print(member)
