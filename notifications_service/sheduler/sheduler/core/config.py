from pydantic import BaseSettings, Field


class BaseConfig(BaseSettings):
    class Config:
        env_file = "./.env"
        env_nested_delimiter = "__"


class DatabaseConfiguration(BaseConfig):
    database: str = Field("postgresql", env="DB_TYPE")
    postgres_user: str = Field("user", env="POSTGRES_USER")
    postgres_password: str = Field("qwerty123", env="POSTGRES_PASSWORD")
    postgres_host: str = Field("127.0.0.1", env="POSTGRES_HOST")
    postgress_port: int = Field(5432, env="POSTGRES_PORT")
    postgres_db: str = Field("auth_base", env="POSTGRES_DB")


class Constants(BaseConfig):
    likes_event_id = Field(1, env="LIKES_EVENT_ID")
    comments_event_id = Field(2, env="COMMENTS_EVENT_ID")
    news_event_id = Field(3, env="NEWS_EVENT_ID")
    ugs_url = Field('localhost:8000/', env="UGS_URL")
    notifications_url = Field('https://localhost:5552', env="NOTIFICATIONS_URL")
    news_url = Field('https://localhost:5552', env="NEWS_URL")


class CeleryConfig(BaseConfig):
    broker_host = Field('localhost', env="BROKER_HOST")
    broker_port = Field('5672', env="BROKER_PORT")
    broker_login = Field('admin', env="BROKER_LOGIN")
    broker_password = Field('password', env="BROKER_PASSWORD")
    task_serializer = 'json'
    result_serializer = 'json'
    accept_content = ['json']
    timezone = 'Europe/Moscow'
    enable_utc = True


class Configuration(BaseConfig):
    db: DatabaseConfiguration = DatabaseConfiguration()
    constants: Constants = Constants()
    celery_config: CeleryConfig = CeleryConfig()


config = Configuration()

db_url = (
    f'{config.db.database}+psycopg2://{config.db.postgres_user}:'
    f'{config.db.postgres_password}@{config.db.postgres_host}:'
    f'{config.db.postgress_port}/{config.db.postgres_db}'
)

broker_url = (
    f'amqp://{config.celery_config.broker_login}:'
    f'{config.celery_config.broker_password}'
    f'@{config.celery_config.broker_host}:'
    f'{config.celery_config.broker_port}'
)
