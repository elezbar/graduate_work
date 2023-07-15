from copy import deepcopy
from uuid import uuid4

import pytest

from utils.token.service import TokenManager, TokenType


@pytest.fixture()
def fake_payload():
    return {"user_id": str(uuid4()), "roles": str(uuid4())}


@pytest.fixture()
def fake_token(fake_payload):
    _fake_payload = deepcopy(fake_payload)
    return TokenManager(TokenType.REFRESH).encode(_fake_payload)
