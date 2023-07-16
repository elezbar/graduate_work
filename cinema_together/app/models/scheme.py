import time
from datetime import datetime
from enum import Enum
from typing import Union, Any
from uuid import UUID

import orjson
from pydantic import BaseModel
from starlette.authentication import SimpleUser

from services.utils import orjson_dumps


class Base(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class RoomUserType(Enum):
    creator = 'creator'
    viewer = 'viewer'


class RoomModel(Base):
    id: UUID | None = None
    film_id: UUID
    creator_id: UUID
    members: list[UUID]


class RoomUserModel(Base):
    id: UUID | None = None
    room_id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        use_enum_values = True


class User(BaseModel):
    id: UUID
    username: str
    first_name: str
    last_name: str


class CustomUser(SimpleUser):
    def __init__(self, _id: str, username: str, first_name: str,
                 last_name: str) -> None:
        super().__init__(username)
        self.id = _id
        self.first_name = first_name
        self.last_name = last_name


class NotificationType(Enum):
    CONNECT = 'connect'
    DISCONNECT = 'disconnect'

    CHAT = 'chat'

    PLAYER_TIMESTAMP = 'PLAYER-timestamp'
    PLAYER_PLAY = 'PLAYER-play'
    PLAYER_PAUSE = 'PLAYER-pause'


class WebsocketMessage(BaseModel):
    type_action: NotificationType
    room_id: UUID | None = None
    connect_id: UUID | None = None
    data: Union[dict, str]
    username: str | None = None
    datetime: int | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.datetime = data.get('datetime', int(time.time()))
