from fastapi import APIRouter, Body, Path, Query

from app.api.exceptions import MemberNotFoundException
from app.exceptions import MemberDoesNotExistException
from app.member import activate_account, get_member_by_username

account_routes = APIRouter()


@account_routes.post('/activate/{username}')
def activate_member_account(password: str = Body(..., embed=True), username: str = Path(...)):
    """
    Activates a member's account

    :param password: Their password
    :param username: Email/phone used during account creation
    :return:
    """
    activate_account(username, password)
    return


@account_routes.get('/auth/accounts')
def check_account_status(username: str = Query(..., embed=True)):
    """
    Returns the account status of the member. Returns a 404 if the member does not exist
    :return:
    """
    try:
        member = get_member_by_username(username)
    except MemberDoesNotExistException:
        raise MemberNotFoundException()

    return {
        'status': member.account.status
    }
