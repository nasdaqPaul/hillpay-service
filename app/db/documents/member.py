from datetime import datetime
from enum import Enum

from bson.objectid import ObjectId
from mongoengine import *


class Role(str, Enum):
    ADMIN = 'admin'
    MEMBER = 'member'


class AccountStatus(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    DISABLED = 'disabled'


class MemberTypeEnum(str, Enum):
    PERMANENT = 'permanent'
    TENANT = 'tenant'


# Imported here to prevent circular imports
from app.db.documents.service import ServiceDocument


class MemberAccountDocument(EmbeddedDocument):
    password = StringField()
    role = EnumField(Role, default=Role.MEMBER)
    status = EnumField(AccountStatus, default=AccountStatus.INACTIVE)


class Bill(EmbeddedDocument):
    _id = ObjectIdField(required=True, default=ObjectId)
    service = LazyReferenceField(ServiceDocument)
    amount = IntField(required=True)

    day = DateField()
    month = StringField()
    year = IntField()

    @property
    def id(self):
        return str(self._id)

    @property
    def service_id(self):
        return str(self.service.id)


class SubscriptionDocument(EmbeddedDocument):
    _id = ObjectIdField(default=ObjectId)
    service = LazyReferenceField(ServiceDocument, null=False)
    subscription_date = DateTimeField(default=datetime.utcnow())

    @property
    def id(self):
        return str(self.service.id)

    @property
    def service_id(self):
        return str(self.service.id)


class MemberDocument(Document):
    first_name = StringField(db_field='firstName')
    last_name = StringField(db_field='lastName')
    phone = StringField()
    email = EmailField()
    account = EmbeddedDocumentField(MemberAccountDocument)
    subscriptions = EmbeddedDocumentListField(SubscriptionDocument)
    bills = ListField(EmbeddedDocumentField(Bill))

    def __init__(self, *args, **kwargs):
        super(MemberDocument, self).__init__(*args, **kwargs)
        self.mpesa = MemberMpesa(self)

    meta = {
        'collection': 'members',
        'indexes': [
            {
                'fields': ['email'],
                'unique': True,
                'partialFilterExpression': {
                    'email': {
                        '$type': 'string'
                    }
                }
            },
            {
                'fields': ['phone'],
                'unique': True,
                'partialFilterExpression': {
                    'phone': {
                        '$type': 'string'
                    }
                }
            }
        ]
    }

    def clean(self):
        """
        Custom validation. Ensures that at least an email or phone number is provided during member insertion
        """
        if (self.phone is None or self.phone == "") and (self.email is None or self.email == ""):
            raise ValidationError('Saving a user document requires at least an email address or a phone number')


class MemberMpesa():
    def __init__(self, member: MemberDocument):
        self.member = member

    def get_account_number(self):
        return self.member.email

    def get_mpesa_number(self):
        return self.member.phone
