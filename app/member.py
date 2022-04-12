from typing import List, Optional

from mongoengine import NotUniqueError
from mongoengine.errors import DoesNotExist
from mongoengine.queryset.visitor import Q

from app.db.documents.member import MemberDocument, MemberAccountDocument, AccountStatus
from app.exceptions import MemberExistsException, MemberDoesNotExistException, AccountAlreadyActive, \
    PhoneNumberNotUniqueException, EmailNotUniqueException
from app.service import Service


class MemberAccount:
    @classmethod
    def from_document(cls, doc: MemberAccountDocument):
        """
        Returns  a member account object from a member account document
        :return:
        """
        account = cls()
        account.password = doc.password
        account.status = doc.status
        account.role = doc.role
        return account


class Member:
    @classmethod
    def from_document(cls, doc: MemberDocument):
        """
        Creates a *member* from a *member_document*

        :return:
        """
        member = cls()
        member.id = str(doc.id)
        member.first_name = doc.first_name
        member.last_name = doc.last_name
        member.email = doc.email
        member.phone = doc.phone
        member.account = MemberAccount.from_document(doc.account)

        return member

    def subscribe(self, service: Service):
        """
        Subscribes the member to a service

        :param service:
        :return:
        """
        pass

    def unsubscribe(self, service: Service):
        """
        Unsubscribes the member from a service

        :param service:
        :return:
        """
        pass

    def add_vehicle(self):
        pass


def get_all_members() -> List[Member]:
    """
    Returns a list of all members in the court

    :return: List[Member]
    """
    all_members = []
    for doc in MemberDocument.objects:
        all_members.append(Member.from_document(doc))
    return all_members


def add_new_member(account: dict, first_name: Optional[str] = None, last_name: Optional[str] = None,
                   phone: Optional[str] = None,
                   email: Optional[str] = None) -> None:
    """
    Adds a new member to the court

    :param account: Account configuration of the user
    :param first_name: Members first name
    :param last_name: Members last name
    :param phone: Members phone number
    :param email: Members email address
    """
    member = MemberDocument(first_name=first_name, last_name=last_name, phone=phone, email=email)
    member_account = MemberAccountDocument(role=account['role'])
    member.account = member_account

    try:
        member.save()
    except NotUniqueError:
        raise MemberExistsException()


# Done to avoid circular imports
from app.auth import hash_password


def activate_account(username: str, password: Optional[str] = None) -> None:
    """
    Activates a members account. Passing in the username and password implies that this is a new activation

    :param username: Email/phone used to create member
    :param password: New password

    :raises AccountAlreadyActiveException: For accounts already created
    :raises MemberDoesNotExistException: For credentials that don't match a member
    """
    try:
        if password:
            member_document = MemberDocument.objects.get(Q(phone=username) | Q(email=username))
            if member_document.account.password:
                raise AccountAlreadyActive()
            else:
                member_document.update(set__account__status=AccountStatus.ACTIVE,
                                       set__account__password=hash_password(password))
        else:
            MemberDocument.objects.get(Q(phone=username) | Q(email=username)).update(
                set__account__status=AccountStatus.ACTIVE)
    except DoesNotExist:
        raise MemberDoesNotExistException()


def get_member_by_username(username: str) -> Member:
    """
    Returns a member

    :param username: Phone or email of the user
    :raises MemberDoesNotExist: Member not found
    :return: Member: Found member
    """
    try:
        member_document = MemberDocument.objects.get(Q(phone=username) | Q(email=username))
    except DoesNotExist:
        raise MemberDoesNotExistException()
    return Member.from_document(member_document)


def set_up_member_account(username: str, password: str, first_name: Optional[str] = None,
                          last_name: Optional[str] = None,
                          phone: Optional[str] = None, email: Optional[str] = None) -> None:
    """
    Attempts to set up a member account.

    :param username: The phone or email that was used in account creation
    :param password: New password
    :param first_name:
    :param last_name:
    :param phone:
    :param email:

    :raises EmailNotUniqueException: Email is already taken
    :raises PhoneNumberNotUniqueException: Phone number already taken
    :raises AccountNotNewException: The account has already been setup
    :raises MemberDoesNotExistException: The username does not correspond to a member
    """
    password_hash = hash_password(password)
    try:
        member_document = MemberDocument.objects.get(Q(phone=username) | Q(email=username))
        # if member_document.account.password:
        #     raise AccountNotNewException()
        member_document.account.password = password_hash
        member_document.account.status = AccountStatus.ACTIVE
        member_document.first_name = first_name
        member_document.last_name = last_name
        member_document.email = email
        member_document.phone = phone

        member_document.save()
    except DoesNotExist:
        raise MemberDoesNotExistException()
    except NotUniqueError as e:
        message = str(e)
        if "phone" in message:
            raise PhoneNumberNotUniqueException()
        else:
            raise EmailNotUniqueException()
