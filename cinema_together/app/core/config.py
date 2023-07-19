import os

from pydantic import BaseSettings


MESSAGE = {
    'type': 'initial_response',
    'condition': 'pause',
    'slider': 0,
    'chat': []
}


class Settings(BaseSettings):
    DEBUG: bool = True

    PROJECT_NAME: str = 'API Проекта "Кино Вместе"'
    PROJECT_HOST: str = '0.0.0.0'
    PROJECT_PORT: int = 8000
    PROJECT_PROTOCOL: str = 'http'

    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_PORT: int = os.getenv('DB_PORT', 5432)
    DB_USERNAME: str = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD: str = os.getenv('DB_PASS', 'postgres')
    DB_NAME: str = os.getenv('DB_NAME')

    JWT_SECRET_KEY: str = os.getenv('SECRET_KEY')
    JWT_ALG: str = os.getenv('ALGORITHM')

    REDIS_HOST: str = os.getenv('REDIS_HOST', 'redis://localhost')
    REDIS_PORT: int = os.getenv('REDIS_PORT', '6379')

    AUTH_URL: str = os.getenv('AUTH_URL', 'http://auth:8001/api/v1/authorizate')
    SECRET: str = os.getenv('SECRET_KEY', 'asdcasdvsdfbsgbdfgbsdfva343')
    ALGORITHM: str = os.getenv('ALGORITHM', 'HS256')

    @property
    def pg_dsn(self):
        return (f'postgresql+asyncpg://{self.DB_USERNAME}:{self.DB_PASSWORD}@'
                f'{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}')  # noqa

    @property
    def get_root_url(self):
        return f'{self.PROJECT_PROTOCOL}://{self.PROJECT_HOST}:{self.PROJECT_PORT}' # noqa

    class Config:
        env_file = '.env'
        case_sensitive = True


settings = Settings()
