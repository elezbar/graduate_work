import logging
from logging import config
import sqlalchemy
import uvicorn

from fastapi import FastAPI, Security, WebSocket
from fastapi.concurrency import run_until_first_complete
from fastapi.responses import ORJSONResponse
from fastapi.security import APIKeyHeader
from redis import asyncio as aioredis

from api.v1 import room
from api.v1.websocket.receiver import chatroom_ws_receiver_test
from api.v1.websocket.sender import chatroom_ws_sender
from models.postgres import Base
from core import cache
from services.room import async_pg_engine
from core.broadcast import broadcast
from core.config import settings
from core.logger import LOGGING


config.dictConfig(LOGGING)

api_key = APIKeyHeader(name='Authorization', auto_error=False)

app = FastAPI(
    title=settings.project_name,
    description='Всё о комнате совместного просмотра',
    version='1.0.0',
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
        f'redis://{settings.redis_host}:{settings.redis_port}'
    )
    await broadcast.connect()
    async with async_pg_engine.begin() as conn:
        sql = sqlalchemy.text(""" select nspname
                  from pg_catalog.pg_namespace
                  where nspname = 'cinema'""")
        if not (await conn.execute(sql)).fetchone():
            await conn.execute(sqlalchemy.schema.CreateSchema('cinema'))
            await conn.run_sync(Base.metadata.create_all)


@app.on_event('shutdown')
async def shutdown() -> None:
    if cache.redis:
        await cache.redis.close()
    await broadcast.disconnect()


@app.websocket('/{chatroom}')
async def chatroom_ws(chatroom: str, websocket: WebSocket):
    print(chatroom)
    await websocket.accept()
    await run_until_first_complete(
        (chatroom_ws_receiver_test, {'websocket': websocket, 'chatroom': chatroom}),
        (chatroom_ws_sender, {'websocket': websocket, 'chatroom': chatroom}),
    )


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.project_host,
        port=settings.project_port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=settings.debug,
    )
