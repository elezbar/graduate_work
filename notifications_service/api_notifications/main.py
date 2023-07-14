
from http import HTTPStatus
import aiohttp
import sqlalchemy
import uvicorn
from api.v1 import (event, notification, send_notification,
                    sended_notification, unsubscribe, wrapper)
from db.base_model import BaseModel
from db.database import engine
from core.config import settings
from core.logger import get_logger
from db import broker
from fastapi import FastAPI, Request, Response
from fastapi.responses import ORJSONResponse
from services.broker.rabbit_broker import RabbitBroker

logger = get_logger(__name__)


app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup() -> None:
    broker.priority_brokers = {
        settings.name_instant_queues: RabbitBroker(
            settings.name_instant_queues,
            settings.broker_login,
            settings.broker_password,
            settings.broker_host,
            settings.broker_port,
        ),
        settings.name_delayed_queues: RabbitBroker(
            settings.name_delayed_queues,
            settings.broker_login,
            settings.broker_password,
            settings.broker_host,
            settings.broker_port,
        ),
    }
    async with engine.begin() as conn:
        sql = sqlalchemy.text(""" select nspname
                  from pg_catalog.pg_namespace
                  where nspname = 'notification'""")
        if not (await conn.execute(sql)).fetchone():
            await conn.execute(sqlalchemy.schema.CreateSchema('notification'))
            await conn.run_sync(BaseModel.metadata.create_all)


@app.on_event('shutdown')
async def shutdown() -> None:
    for _, b in broker.priority_brokers.items():
        print(b)
        b.close()


# @app.middleware("http")
# async def auth_middleware(request: Request, call_next):
#     if request.url.path in [app.docs_url, app.openapi_url]:
#         return await call_next(request)
#     headers = request.headers
#     async with aiohttp.ClientSession() as client:
#         resp = await client.get(settings.auth_url, headers=headers)
#         if resp.status == 200:
#             response = await call_next(request)
#             return response
#         return Response(status_code=HTTPStatus.UNAUTHORIZED)


app.include_router(event.router, prefix='/api/v1/event', tags=['event'])
app.include_router(notification.router, prefix='/api/v1/notification', tags=['notification'])
app.include_router(send_notification.router, prefix='/api/v1/send_notification', tags=['send_notification'])
app.include_router(unsubscribe.router, prefix='/api/v1/unsubscribe', tags=['unsubscribe'])
app.include_router(wrapper.router, prefix='/api/v1/wrapper', tags=['wrapper'])
app.include_router(sended_notification.router, prefix='/api/v1/sended_notification', tags=['sended_notification'])

if __name__ == '__main__':
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=True)
