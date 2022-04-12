from typing import Optional

from mongoengine.errors import DoesNotExist
from mongoengine.queryset.visitor import Q
from passlib.context import CryptContext

from app.db.documents.member import MemberDocument
from app.member import Member

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> str:
    """
    Encrypts a password

    :param password: Plain-text password
    :return: Encrypted password
    """
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verifies password and its hash

    :param password: Plain-Text password
    :param password_hash: Encrypted password
    :return: bool:
    """
    return pwd_context.verify(password, password_hash)


def authenticate_member(username: str, password: str) -> Optional[Member]:
    """
    Authenticates a member by their phone number or email address
    It returns a *member* on successful authentication and None otherwise

    :param username: A member's unique email or phone number
    :param password: A member's password
    :return: Member: Found member
    :return: None: Failed authentication
    """
    try:
        member_document = MemberDocument.objects.get(Q(phone=username) | Q(email=username))
    except DoesNotExist:
        return None
    if not verify_password(password, member_document.account.password):
        return None
    return Member.from_document(member_document)
