import aiohttp
import functools
import json

from fastapi import HTTPException, status

from core.config import settings


def login_required():
    def wrapper(func):
        @functools.wraps(func)
        async def inner(*args, **kwargs):
            token = kwargs.get('Authorization')
            room = kwargs.get('room')
            payload = {
                "RequestedObjTypes": "movie",
                "RequestType": "get",
                "RequestedObjId": str(room.film_id)
            }
            async with aiohttp.ClientSession() as client:
                try:
                    resp = await client.post(f'{settings.AUTH_URL}/authorizate', json=payload, headers={
                        'Authorization': token
                    })
                    if resp.status == 200:
                        return await func(*args, **kwargs)
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail='Без авторизации никак!')
                except aiohttp.client_exceptions.InvalidURL:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail='Не найден сервис авторизации!')
        return inner
    return wrapper
