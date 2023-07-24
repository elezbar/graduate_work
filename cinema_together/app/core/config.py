import os

from pydantic import BaseSettings, Field


MESSAGE = {
    'type': 'initial_response',
    'condition': 'pause',
    'slider': 0,
    'chat': []
}


class Settings(BaseSettings):
    debug: bool = True

    project_name: str = 'API Проекта "Кино Вместе"'
    project_host: str = '0.0.0.0'
    project_port: int = 8000
    project_protocol: str = 'http'

    postgres_host: str = 'localhost'
    postgres_port: int = 5432
    postgres_user: str = 'postgres'
    postgres_password: str = 'postgres'
    postgres_db: str = ...

    jwt_secret_key: str = Field(..., env='SECRET_KEY')
    jwt_alg: str = Field(..., env='ALGORITHM')

    redis_host: str = 'redis://localhost'
    redis_port: int = 6379

    auth_url: str = 'http://auth:8001/api/v1/authorizate'
    secret: str = Field('asdcasdvsdfbsgbdfgbsdfva343', env='SECRET_KEY')
    algorithm: str = 'HS256'
    notification_url: str = 'http://notifications:8002/api/v1/send_notification/send_notification/delayed'

    @property
    def pg_dsn(self):
        return (f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
                f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}')  # noqa

    @property
    def get_root_url(self):
        return f'{self.PROJECT_PROTOCOL}://{self.PROJECT_HOST}:{self.PROJECT_PORT}' # noqa

    class Config:
        env_file = '.env'
        case_sensitive = True


settings = Settings()
