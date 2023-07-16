import aiohttp
import functools

from fastapi import HTTPException, status


def login_required():
    def wrapper(func):
        @functools.wraps(func)
        async def inner(*args, **kwargs):
            request = kwargs.get('request')
            room = kwargs.get('room')
            payload = {
                "RequestedObjTypes": "movie",
                "RequestType": "get",
                "RequestedObjId": room.film_id
            }
            headers = request.headers
            async with aiohttp.ClientSession() as client:
                resp = await client.post('http://127.0.0.1:8001/api/v1/authorizate', data=payload, headers=headers)
                if resp.status == 200:
                    return await func(*args, **kwargs)
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail='Без авторизации никак!')

        return inner

    return wrapper
