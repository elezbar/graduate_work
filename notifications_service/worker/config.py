from pydantic import BaseSettings, Field


class BaseConfig(BaseSettings):
    class Config:
        env_file = "./.env"
        env_nested_delimiter = "__"


class BrokerConf(BaseConfig):
    name_instant_queue: str = Field("queue1", env="NAME_INSTANT_QUEUE")
    name_delayed_queue: str = Field("queue1", env="NAME_DELAYED_QUEUE")
    broker_login: str = Field("admin", env="BROKER_LOGIN")
    broker_password: str = Field("password", env="BROKER_PASSWORD")
    broker_host: str = Field("localhost", env="BROKER_HOST")
    broker_port: int = Field(2128, env="BROKER_PORT")
    access_token: str = Field("access_token", env="ACCESS_TOKEN")


class SMTPConf(BaseConfig):
    smtp_host: str = Field("localhost", env="SMTP_HOST")
    smtp_port: int = Field(1025, env="SMTP_PORT")
    smtp_login: str = Field("admin", env="SMTP_LOGIN")
    smtp_password: str = Field("password", env="SMTP_PASSWORD")


class ConstantsConf(BaseConfig):
    access_token: str = Field("random_token_is_here", env="ACCESS_TOKEN")
    url_get_user: str = Field("user", env="URL_GET_USER")
    email_from: str = Field("bill@microsoft.com", env="EMAIL_FROM")


class Configuration(BaseConfig):
    broker: BrokerConf = BrokerConf()
    smtp: SMTPConf = SMTPConf()
    constants: ConstantsConf = ConstantsConf()


config = Configuration()
