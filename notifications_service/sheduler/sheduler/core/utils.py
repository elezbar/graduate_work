import aiohttp
import orjson

from aiohttp.client_exceptions import ClientError


def camelcase_to_snake(val: str) -> str:
    """
    Converts CamelCaseString to stake_case_string
    """
    if not val:
        return val
    new_val = [val[0].lower()]
    for v in val[1:]:
        new_val.append(v if not v.isalpha() or v.islower() else f"_{v.lower()}")
    return "".join(new_val)


async def request_get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            try:
                pokemon = await resp.json()
                return pokemon
            except ClientError as e:
                pass
            finally:
                return False


async def request_post(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url,
            data = orjson.dumps(data).encode(),
            headers = {}
        ) as resp:
            try:
                pokemon = await resp.json()
                return pokemon
            except ClientError as e:
                pass
            finally:
                return False
