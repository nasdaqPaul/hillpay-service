from typing import List

from fastapi import APIRouter, HTTPException, Query

from app.api.models import MemberResponseModel, MemberModel
from app.api.models.member import MemberSetupModel
from app.exceptions import MemberExistsException, EmailNotUniqueException, PhoneNumberNotUniqueException
from app.member import get_all_members, add_new_member, set_up_member_account

member_routes = APIRouter()


@member_routes.post("/court/members", status_code=201)
def add_member(new_member: MemberModel):
    """
    Adds a new member to the court. Endpoint requires authentication and authorization.
    """
    try:
        add_new_member(**new_member.dict(exclude_none=True))
    except MemberExistsException:
        raise HTTPException(status_code=409, detail='A member with the provided credentials already exists.')
    return


@member_routes.get("/court/members", response_model=List[MemberResponseModel], response_model_exclude_none=True)
def get_members():
    """
    Returns a list of members. Endpoint requires authentication and authorization.
    """
    all_members = get_all_members()
    return [MemberResponseModel.from_orm(member).dict() for member in all_members]


@member_routes.post("/set-up/member")
def set_up_member_account(member: MemberSetupModel, username: str = Query(...)):
    """
    Sets up a member's account, by enabling it and setting its password
    :return:
    """
    creds = [member.phone, member.email]
    if username not in creds:
        raise Exception()
    try:
        parsed = member.dict(exclude_none=True)
        password = parsed['account']['password']
        parsed.pop('account')
        set_up_member_account(username=username, password=password, **parsed)
    except EmailNotUniqueException as e:
        print("email")
    except PhoneNumberNotUniqueException as e:
        print("phone")
    return
