import logging
from logging import config

import uvicorn
from fastapi import FastAPI, Security
from fastapi.responses import ORJSONResponse
from fastapi.security import APIKeyHeader

from api.v1 import room
from core.config import settings
from core.logger import LOGGING

config.dictConfig(LOGGING)

api_key = APIKeyHeader(name='authorization', auto_error=False)

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
# TODO: для auth с проверкой токенов нужен ещё код (мидлвара?)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.PROJECT_HOST,
        port=settings.PROJECT_PORT,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=settings.DEBUG,
    )
