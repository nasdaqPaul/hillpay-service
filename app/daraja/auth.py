from datetime import datetime, timedelta
import json
import requests
from jose import jws

from app.daraja.config import daraja_config
from app.daraja.helpers import encode

_access_token = None
_expires_time = None


def verify_request_signature(signature: str):
    return json.loads(jws.verify(signature, daraja_config.jws_secret, algorithms=['HS256']))


def sign_request(payload: dict) -> str:
    """
    Signs a payment request

    :param payload:
    :return:
    """
    return jws.sign(payload, daraja_config.jws_secret, algorithm='HS256')


def get_access_token() -> str:
    if not access_token_is_valid():
        refresh_access_token()
    return _access_token


def refresh_access_token():
    global _expires_time
    global _access_token

    password = encode(f"{daraja_config.consumer_key}:{daraja_config.consumer_secret}")
    response = requests.request(
        "GET",
        'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials',
        headers={'Authorization': f'Basic {password}'})
    token = response.json()
    _expires_time = datetime.now() + timedelta(seconds=int(token['expires_in']))
    _access_token = token['access_token']


def access_token_is_valid():
    return _access_token and datetime.now() < _expires_time
