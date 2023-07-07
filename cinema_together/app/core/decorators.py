import functools

from fastapi import HTTPException, status


def login_required():
    def wrapper(func):
        @functools.wraps(func)
        async def inner(*args, **kwargs):
            request = kwargs.get('request')
            user = getattr(request, 'user', None)
            is_auth = getattr(user, 'is_authenticated', False)
            if not request or not is_auth:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail='Без логина никак!')
            return await func(*args, **kwargs)

        return inner

    return wrapper
