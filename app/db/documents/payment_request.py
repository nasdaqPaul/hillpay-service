from mongoengine import *

from app.db.documents.member import MemberDocument


class PaymentRequestDocument(Document):
    member = LazyReferenceField(MemberDocument)
    bills = ListField(ObjectIdField())
    amount = IntField()

    # @property
    # def id(self):
    #     return str(self.id)

    @property
    def member_id(self):
        return str(self.member.id)
    meta = {
        "collection": "paymentRequests"
    }
