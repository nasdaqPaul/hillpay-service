from typing import List

from app.db.documents.member import MemberDocument


def settle_bills(member_id: str, bills: List[str]):
    """
    Settle member bills
    :param member_id:
    :param bills:
    :return:
    """

    member = MemberDocument.objects.get(id=member_id)
    