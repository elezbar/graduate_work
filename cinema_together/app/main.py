from http import HTTPStatus
import logging
from logging import config
import aiohttp
import uvicorn

from fastapi import FastAPI, Request, Response, Security, WebSocket
from fastapi.concurrency import run_until_first_complete
from fastapi.responses import ORJSONResponse
from fastapi.security import APIKeyHeader
from redis import asyncio as aioredis

from api.v1 import room
# from api.v1.websocket.receiver import chatroom_ws_receiver
from api.v1.websocket.receiver import chatroom_ws_receiver_test
from api.v1.websocket.sender import chatroom_ws_sender
from core import cache
from core.broadcast import broadcast
from core.config import settings
from core.logger import LOGGING


config.dictConfig(LOGGING)

api_key = APIKeyHeader(name='Authorization', auto_error=False)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Всё о комнате совместного просмотра",
    version="1.0.0",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(
    room.router, prefix='/api/v1/room', tags=['Room'],
    dependencies=[Security(api_key)]
)


@app.on_event('startup')
async def startup() -> None:
    cache.redis = aioredis.from_url(
        f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}'
    )
    await broadcast.connect()


@app.on_event('shutdown')
async def shutdown() -> None:
    if cache.redis:
        await cache.redis.close()
    await broadcast.disconnect()


@app.websocket("/{chatroom}")
async def chatroom_ws(chatroom: str, websocket: WebSocket):
    await websocket.accept()
    await run_until_first_complete(
        (chatroom_ws_receiver_test, {"websocket": websocket, 'chatroom': chatroom}),
        (chatroom_ws_sender, {"websocket": websocket, 'chatroom': chatroom}),
    )


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.PROJECT_HOST,
        port=settings.PROJECT_PORT,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=settings.DEBUG,
    )
