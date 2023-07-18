import jwt
import orjson
import random
import string

from uuid import UUID

from core.config import MESSAGE, settings
from core.cache import get_redis, Redis


def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


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


async def modify_cached_message(chatroom, event_message, cached_message):
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
            if len(cached_message['chat']) == 21:
                message_to_arch = cached_message['chat'].pop(0)
                archive = await get_cache(f'{chatroom}-archive')
                if not archive:
                    archive = []
                archive.insert(0, message_to_arch)
                await set_cache(f'{chatroom}-archive', archive)  
    elif event_message['type'] == 'initial_request':
        cached_message['username'] = event_message['username']
    return cached_message


async def messages_paginator(chatroom, event_message, cached_message):
    archive = await get_cache(f'{chatroom}-archive')
    if archive:
        page = int(event_message['page'])
        quantity = page * 20
        messages = archive[0, quantity]
        for message in messages:
            cached_message['chat'].append({
                'username': message['username'], 
                'message': message['message']
            })
        return cached_message


async def set_cached_message(chatroom, message):
    rd = get_redis()
    redis = Redis(rd)
    await redis.set(f'{chatroom}-007', message)


async def set_cache(key, value):
    rd = get_redis()
    redis = Redis(rd)
    await redis.set(key, value)


async def get_cache(key):
    rd = get_redis()
    redis = Redis(rd)
    await redis.get(key)


async def check_temp_token(message: dict, rs) -> dict | bool:
    """Проверка токена."""
    if rs:
        token = message['token']
        if message['type'] == 'initial_request':
            saved_token = rs.check_token(message['room_id'], message['user_id'], token)
        else:
            saved_token = await get_cache(message['user_id'])
        if (token == saved_token):
            new_token = get_random_string(16)
            await set_cache(message['user_id'], new_token)
            return new_token
    else:
        return 'qwerty1234567'
