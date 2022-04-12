from typing import Optional

from fastapi import Header, WebSocket, status
from jose import jwt


async def get_access_token(websocket: WebSocket, authorization: Optional[str] = Header(None)) -> str:
    if authorization is None:
        print('No auth')
        await websocket.close(code=status.WS_1000_NORMAL_CLOSURE)
    return authorization


def get_authenticated_member(access_token: str):
    return jwt.decode(access_token, 'some random string', algorithms=['HS256'])
