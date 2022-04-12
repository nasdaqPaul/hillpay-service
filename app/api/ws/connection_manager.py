from typing import List, Tuple

from fastapi import WebSocket


def find_member_connections(member_id: str):
    def f(con_tuple):
        if con_tuple[0] == member_id:
            return True
        else:
            return False

    return f


class ConnectionManager:
    def __init__(self):
        self._connections: List[Tuple[str, WebSocket]] = []

    def connect(self, member_id: str, connection: WebSocket):
        self._connections.append((member_id, connection))

    def disconnect(self, member_id: str, connection: WebSocket):
        self._connections.remove((member_id, connection))
        print(self._connections)

    async def send_json(self, member_id: str, payload: dict):
        for con_tuple in filter(find_member_connections(member_id), self._connections):
            await con_tuple[1].send_json(payload)

    async def broadcast_message(self, message: str):
        for con_tuple in self._connections:
            await con_tuple[1].send_json({'message': 'Test Message'})
