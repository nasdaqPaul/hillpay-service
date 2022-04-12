class MemberExistsException(Exception):
    """
    Exception raised when creating a member with credentials of another member
    """
    pass


class MemberDoesNotExistException(Exception):
    """

    """


class AccountAlreadyActive(Exception):
    """
    Exception raised when a trying to activate an active account
    """
    pass


class EmailNotUniqueException(Exception):
    pass


class PhoneNumberNotUniqueException(Exception):
    pass


class AccountNotNewException(Exception):
    pass

class BillInPaymentRequestException(Exception):
    pass