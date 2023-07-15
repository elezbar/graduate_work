from enum import Enum

from pydantic import BaseSettings, Field


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"


METHOD_TO_CRUD = {"post": "create", "get": "read", "put": "update", "patch": "update", "delete": "delete"}


class CRUD(Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"


class BaseRoles(Enum):
    ANONIMOUS = "eaa259ca-1b78-41f8-a345-38411a65803b"
    REGULAR = "78879608-0148-4f3e-9e16-356994d989d2"
    SUBSCRIBER = "4cbf2021-8505-420a-af6f-1bf8bb1689aa"
    MANGER = "f70a78f6-fb93-4a47-b8eb-e325211ad4e9"
    SUPERUSER = "f8f5ee59-af86-4fd3-a11f-75d233dbd7fa"


class TYPES_WITH_ID(Enum):
    MOVIE = "movie"
    GENRE = "genre"
    PERSON = "person"
    USER = "user"
    ROLE = "role"


# class PERMISSION_OBJECTS_IDS(Enum):
#     MOVIE = 'e3750427-731c-4f02-a481-6567e1c68760'
#     PERSON = '16675179-39cf-4460-87ae-fadc0556d62d'
#     GENRE = '155d4bce-3df7-4724-b659-c50bf0a090b8'
#     USER = '87591157-bd60-45fb-840e-f7266f4db5c7'
#     PERMISSION = '155d4bce-3df7-4724-b659-c50bf0a090b8'
#     ROLE = '155d4bce-3df7-4724-b659-c50bf0a090b8'


class BaseConfig(BaseSettings):
    class Config:
        env_file = "./.env"
        env_nested_delimiter = "__"


class PasswordConfiguration(BaseConfig):
    hash_method: str = Field("pbkdf2:sha256", env="HASH_METHOD")
    salt_length: int = Field(16, env="SALT_LENGTH")


class TokenExpiringConfiguration(BaseConfig):
    access: int = Field(15, env="ACCESS_EXPIRED")
    refresh: int = Field(4320, env="REFRESH_EXPIRED")


class TokenConfiguration(BaseConfig):
    secret: str = Field("fake_secret_code_fake_secret_code", env="SECRET_KEY")
    algorithm: str = Field("HS256", env="ALGORITHM")
    expiring: TokenExpiringConfiguration = TokenExpiringConfiguration()


class SecurityConfiguration(BaseConfig):
    token: TokenConfiguration = TokenConfiguration()
    password: PasswordConfiguration = PasswordConfiguration()


class DatabaseConfiguration(BaseConfig):
    database: str = Field("postgresql", env="DB_TYPE")
    postgres_user: str = Field("user", env="POSTGRES_USER")
    postgres_password: str = Field("qwerty123", env="POSTGRES_PASSWORD")
    postgres_host: str = Field("127.0.0.1", env="POSTGRES_HOST")
    postgress_port: int = Field(5432, env="POSTGRES_PORT")
    postgres_db: str = Field("auth_base", env="POSTGRES_DB")


class CacheConfiguration(BaseConfig):
    redis_host: str = Field("redis", env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")
    cache_time_default: int = Field(3600, env="CACHE_TIME_DEFAULT")
    base_cache_expire_in_seconds: int = Field(300, env="BASE_CACHE_EXPIRE_IN_SECONDS")
    cache_prefix_to_find: str = "cache_prefix_to_find-"


class FlaskConfiguration(BaseConfig):
    DEBUG: bool = Field(False, env="DEBUG")
    TESTING: bool = Field(False, env="TESTING")
    HOST: str = Field("0.0.0.0", env="FLASK_HOST")
    PORT: int = Field(5000, env="FLASK_PORT")
    SWAGGER: dict = {
        "swagger": "2.0",
        "info": {
            "title": "Flask Restful Swagger Demo",
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": 'JWT Authorization header using the Bearer scheme. Example: "Authorization: {token}"',
            }
        },
        "security": [{"Bearer": []}],
    }


class Configuration(BaseConfig):
    secret: str = Field("fake_secret_code_fake_secret_code", env="SECRET_KEY")
    flask: FlaskConfiguration = FlaskConfiguration()
    security: SecurityConfiguration = SecurityConfiguration()
    db: DatabaseConfiguration = DatabaseConfiguration()
    cache: CacheConfiguration = CacheConfiguration()


config = Configuration()

db_url = (
    f"{config.db.database}+psycopg2://{config.db.postgres_user}:"
    f"{config.db.postgres_password}@{config.db.postgres_host}:"
    f"{config.db.postgress_port}/{config.db.postgres_db}"
)

redis_url = f"redis://{config.cache.redis_host}:" f"{config.cache.redis_port}"
