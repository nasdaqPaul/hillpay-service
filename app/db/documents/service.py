from enum import Enum

from mongoengine import *

from app.db.documents.member import MemberTypeEnum


class BillingIntervalEnum(str, Enum):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    ANNUALLY = 'annually'


class ServiceStatusEnum(str, Enum):
    ACTIVE = 'active'
    SUSPENDED = 'suspended'


class ServiceModelEnum(str, Enum):
    RENEWABLE = 'renewable'
    ON_DEMAND = 'on-demand'


class ServiceBillingDocument(EmbeddedDocument):
    interval = EnumField(BillingIntervalEnum, default=BillingIntervalEnum.MONTHLY)
    # The amount is assumed to be in KSH, with no fraction parts
    amount = IntField(required=True, min_value=0)


class ServiceDocument(Document):
    name = StringField(required=True)
    description = StringField()
    billing = EmbeddedDocumentField(ServiceBillingDocument)
    eligibility = ListField(choices=[e.value for e in MemberTypeEnum], default=[e.value for e in MemberTypeEnum])
    status = EnumField(ServiceStatusEnum, default=ServiceStatusEnum.ACTIVE)
    model = EnumField(ServiceModelEnum, default=ServiceModelEnum.RENEWABLE)

    meta = {
        "collection": "services"
    }
