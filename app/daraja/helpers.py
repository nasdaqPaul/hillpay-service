import base64
from datetime import datetime

import requests


def encode(s):
    b = s.encode('ascii')
    m_b = base64.b64encode(b)
    m = m_b.decode('ascii')
    return m


def decode(s):
    b = s.encode('ascii')
    m_b = base64.b64decode(b)
    m = m_b.decode('ascii')
    return m


def get_time_stamp():
    return datetime.now().strftime('%Y%m%d%H%m%S')


def get_access_token(consumer_key: str, secret_key: str):
    password = encode(f"{consumer_key}:{secret_key}")
    response = requests.request(
        "GET",
        'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials',
        headers={'Authorization': f'Basic {password}'})
    return response.json()
