import jwt
import orjson

from uuid import UUID

from core.config import MESSAGE, settings
from core.cache import get_redis, Redis

def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


def create_room_link(room_id: UUID):
    return f'{settings.get_root_url}/api/v1/room/{str(room_id)}/join'


async def get_cached_message(chatroom):
    rd = get_redis()
    redis = Redis(rd)
    cached_message = await redis.get(f'{chatroom}-007')
    if not cached_message:
        cached_message = MESSAGE
    return cached_message


async def modify_cached_message(event_message, cached_message):
    if event_message['type'] not in ['initial_request', 'initial_response']:
        if event_message['type'] == 'play':
            cached_message['condition'] = 'play'
        if event_message['type'] == 'pause':
            cached_message['condition'] = 'pause'
        if event_message['type'] == 'slider':
            cached_message['slider'] = event_message['value']
        if event_message['type'] == 'message':
            cached_message['chat'].append({
                'username': event_message['username'],
                'message': event_message['message']
            })
    elif event_message['type'] == 'initial_request':
        cached_message['username'] = event_message['username']
    return cached_message


async def set_cached_message(chatroom, message):
    rd = get_redis()
    redis = Redis(rd)
    await redis.set(f'{chatroom}-007', message)


def decode_token(token: str) -> dict | bool:
    """Расшифровка токена в словарь."""
    try:
        decoded: dict = jwt.decode(jwt=token, key=settings.SECRET, algorithms=[settings.ALGORITHM])
        return decoded
    except (
        jwt.exceptions.ImmatureSignatureError,
        jwt.exceptions.ExpiredSignatureError,
        jwt.exceptions.InvalidSignatureError,
    ):
        return False
