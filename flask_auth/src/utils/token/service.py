import datetime as dt

import jwt

from core.config import TokenType, config
from models.models_pydantic import Payload

TOKEN_EXPIRE_IN = {
    TokenType.ACCESS: dt.timedelta(days=config.security.token.expiring.access),
    TokenType.REFRESH: dt.timedelta(days=config.security.token.expiring.refresh),
}


class TokenManager:
    secret: str = config.security.token.secret
    algorithm: str = config.security.token.algorithm

    def __init__(self, token_type: TokenType):
        self.token_type: TokenType = token_type

    def _get_additional_info(self) -> dict:
        """Возвращает технические поля для payload токена."""
        now: dt.datetime = dt.datetime.now(dt.timezone.utc) - dt.timedelta(seconds=1)

        return {
            "iat": now.timestamp(),  # Дата и время выдачи токена
            "exp": (now + TOKEN_EXPIRE_IN[self.token_type]).timestamp(),  # Дата и время истечения срока жизни токена
            "token_type": self.token_type.value,
        }

    @staticmethod
    def _timestamp_to_datetime(decoded: dict) -> dict:
        """Преобразуем timestamp-значения в читаемый datetime."""

        datetime_keys = ("iat", "exp")

        filtered = list(filter(lambda key: decoded.get(key) is not None, datetime_keys))

        decoded.update({key: dt.datetime.fromtimestamp(decoded[key]) for key in filtered})

        return decoded

    def encode(self, payload: dict) -> str:
        """Создание токена из словаря."""

        payload.update(self._get_additional_info())  # Дополняем словарь технической информацией

        try:
            token = jwt.encode(payload=payload, key=self.secret, algorithm=self.algorithm)

        except jwt.exceptions.ImmatureSignatureError:
            return ""

        return token

    @classmethod
    def decode(cls, token: str) -> Payload | bool:
        """Расшифровка токена в словарь."""
        try:
            decoded: dict = jwt.decode(jwt=token, key=cls.secret, algorithms=[cls.algorithm])
            decoded = cls._timestamp_to_datetime(decoded)  # Преобразуем timestamp-поля в читаемый datetime
            decoded["roles"] = decoded["roles"].split(", ")
            return Payload(**decoded)
        except (
            jwt.exceptions.ImmatureSignatureError,
            jwt.exceptions.ExpiredSignatureError,
            jwt.exceptions.InvalidSignatureError,
        ):
            return False

    @classmethod
    def base64_decode(cls, token: str) -> Payload | bool:
        """Расшифровка токена в словарь."""

        try:
            decoded: dict = jwt.decode(token, options={"verify_signature": False})
            decoded = cls._timestamp_to_datetime(decoded)  # Преобразуем timestamp-поля в читаемый datetime
            return Payload(**decoded)
        except (
            jwt.exceptions.ImmatureSignatureError,
            jwt.exceptions.ExpiredSignatureError,
        ):
            return False
