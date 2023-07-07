from uuid import UUID

import orjson

from core.config import settings


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


def create_room_link(room_id: UUID):
    return f'{settings.get_root_url}/api/v1/room/{str(room_id)}/join'
