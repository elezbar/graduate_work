import pytest

from utils.passwords.service import PasswordManager


@pytest.fixture()
def fake_password():
    return "fake_password"


@pytest.fixture()
def fake_hash(fake_password):
    return PasswordManager.generate_hash(fake_password)
