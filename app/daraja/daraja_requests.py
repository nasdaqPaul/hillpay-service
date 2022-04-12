from typing import Optional

import requests

from app.daraja.auth import sign_request, get_access_token
from app.daraja.config import daraja_config
from app.daraja.helpers import encode, get_time_stamp


def queue_stk_request(phone_number: int, amount: int, account_number: str, jws_payload: Optional[any] = None,
                      callback_endpoint: Optional[str] = None):
    time_stamp = get_time_stamp()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {get_access_token()}'
    }

    callback_url = daraja_config.webhook_url
    if callback_endpoint and jws_payload:
        callback_url = f"{callback_url}/{callback_endpoint}/{sign_request(jws_payload)}"
    elif callback_endpoint and not jws_payload:
        callback_url = f"{callback_url}/{callback_endpoint}"
    elif jws_payload and not callback_endpoint:
        callback_url = f"{callback_url}/{sign_request(jws_payload)}"

    payload = {
        "BusinessShortCode": 174379,
        "Password": encode(f"174379{daraja_config.passkey}{time_stamp}"),
        "Timestamp": time_stamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": 174379,
        "PhoneNumber": phone_number,
        "CallBackURL": callback_url,
        "AccountReference": account_number,
        "TransactionDesc": "Payment of Gate Pass"
    }
    response = requests.request(
        "POST",
        f'{daraja_config.daraja_url}/mpesa/stkpush/v1/processrequest',
        json=payload,
        headers=headers
    )
    return response.json()
