import pytest

from models.models_pydantic import Payload
from utils.token.service import TokenManager, TokenType


@pytest.mark.token_manager
@pytest.mark.parametrize("token_type", [TokenType.ACCESS, TokenType.REFRESH])
def test_encode_token(token_type, fake_payload):
    token = TokenManager(token_type).encode(fake_payload)

    # Проверяем возвращаемый тип
    assert isinstance(token, str)

    # Проверяем, что длина больше 0
    assert len(token) > 0

    # Проверяем, что токен состоит из трёх частей через точку
    assert len(token.split(".")) == 3


@pytest.mark.token_manager
def test_decode_token(fake_payload, fake_token):
    decoded = TokenManager.decode(fake_token)

    # Проверяем возвращаемый тип
    assert isinstance(decoded, Payload)

    # Проверяем наличие ключей из оригинального payload
    assert set(fake_payload.keys()).issubset(set(decoded.dict().keys()))
