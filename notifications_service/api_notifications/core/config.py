import os
from logging import config as logging_config

from pydantic import BaseSettings, Field

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    host: str = Field('0.0.0.0', env='NOTIFY_HOST')
    port: int = Field(8002, env='NOTIFY_PORT')
    project_name: str = Field('notification', env='PROJECT_NAME')
    name_instant_queues: str = Field('INSTANT_QUEUE', env='NAME_INSTANT_QUEUE')
    name_delayed_queues: str = Field('DELAYED_QUEUE', env='NAME_DELAYED_QUEUE')
    broker_login: str = Field('guest', env='BROKER_LOGIN')
    broker_password: str = Field('guest', env='BROKER_PASSWORD')
    broker_host: str = Field('rabbitmq', env='BROKER_HOST')
    broker_port: int = Field(5672, env='BROKER_PORT')
    auth_url: str = Field('auth_service', env='AUTH_URL')
    db_type = Field('postgresql', env='DB_TYPE')
    postgres_user: str = Field('app', env='POSTGRES_USER')
    postgres_password: str = Field('123qwe', env='POSTGRES_PASSWORD')
    postgres_host: str = Field('db', env='POSTGRES_HOST')
    postgres_port: int = Field(5432, env='POSTGRES_PORT')
    postgres_db: str = Field('notification_database', env='POSTGRES_DB')

    class Config:
        env_file = "./.env"
        env_file_encoding = 'utf-8'
        env_nested_delimiter = "__"


settings = Settings.construct()
