from typing import Optional

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from jose.exceptions import ExpiredSignatureError

from app.api.ws.auth import get_authenticated_member, get_access_token
from app.api.ws.connection_manager import ConnectionManager

ws_router = APIRouter()
manager = ConnectionManager()


@ws_router.websocket('/ws')
async def ws_endpoint(websocket: WebSocket, token: Optional[str] = Query(None)):
    await websocket.accept()
    if token is None:
        await websocket.close(4003)
        return
    try:
        member = get_authenticated_member(token)
    except ExpiredSignatureError:
        await websocket.close(code=4004)
        return
    manager.connect(member['id'], websocket)
    try:
        while True:
            client_message = await websocket.receive_json()
            print(client_message)
    except WebSocketDisconnect as e:
        manager.disconnect(member['id'], websocket)

