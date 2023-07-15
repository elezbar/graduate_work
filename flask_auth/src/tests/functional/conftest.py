import pytest

from app import create_app
from db.alchemy import DBSession
from utils.token.service import TokenManager, TokenType


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def session(app):
    session = DBSession()
    yield session
    session.close()


@pytest.fixture()
def access(app):
    payload = {"user_id": "e5fcf716-4121-4b64-b23b-b6d63a14a850", "roles": "f8f5ee59-af86-4fd3-a11f-75d233dbd7fa"}
    access = TokenManager(TokenType.ACCESS).encode(payload)

    yield access
