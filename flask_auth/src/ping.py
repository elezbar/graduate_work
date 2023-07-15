import psycopg2
import redis

from contextlib import contextmanager
from psycopg2.extensions import connection
from psycopg2.extras import DictCursor
from pydantic import BaseSettings, Field

from core.config import config
from core.backoff import backoff_function


@contextmanager
def pg_conn_context(dsl: dict) -> connection:
    conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    yield conn
    conn.close()


class DatabaseConfiguration(BaseSettings):
    database: str = Field("auth_base", env="POSTGRES_DB")
    user: str = Field("user", env="POSTGRES_USER")
    password: str = Field("qwerty123", env="POSTGRES_PASSWORD")
    host: str = Field("127.0.0.1", env="POSTGRES_HOST")
    port: int = Field(5432, env="POSTGRES_PORT")

    class Config:
        env_file = './.env'
        env_file_encoding = 'utf-8'


class Ping:

    @backoff_function()
    def ping_db(self):
        with (pg_conn_context(DatabaseConfiguration().dict()) as pg_conn):
            cur = pg_conn.cursor()
            cur.execute('SELECT 1;')
            cur.fetchone()
            cur.close()

    @backoff_function
    def ping_redis(self):
        r = redis.Redis(host=config.cache.redis_host, port=config.cache.redis_port,
                        decode_responses=True)
        r.ping()
        r.close()


if __name__ == '__main__':
    ping = Ping()
    ping.ping_db()
    ping.ping_redis()
