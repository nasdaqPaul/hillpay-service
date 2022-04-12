from app.db.documents.member import MemberDocument, Bill


def bil(service, member: MemberDocument):
    # Check if member has already been billed for this service
    for bill in member.bills:
        if bill.service.id == service.id:
            return
    member.bills.append(Bill(service=service))


for member in MemberDocument.objects:
    if member.subscriptions:
        for sub in member.subscriptions:
            bil(sub, member)
    member.save()
