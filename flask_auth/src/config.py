# coding=utf-8
from pydantic import BaseModel, BaseSettings


class PasswordConfiguration(BaseModel):
    hash_method: str = "pbkdf2:sha256"
    salt_length: int = 16


class TokenExpiringConfiguration(BaseModel):
    access: int = 1
    refresh: int = 30


class TokenConfiguration(BaseModel):
    secret: str = "secret"
    algorithm: str = "HS256"
    expiring: TokenExpiringConfiguration = TokenExpiringConfiguration()


class SecurityConfiguration(BaseModel):
    token: TokenConfiguration = TokenConfiguration()
    password: PasswordConfiguration = PasswordConfiguration()


class Configuration(BaseSettings):
    security: SecurityConfiguration = SecurityConfiguration()

    class Config:
        env_file = "./.env"
        env_nested_delimiter = "__"


config = Configuration()
