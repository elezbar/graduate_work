import pytest

from utils.passwords.service import PasswordManager


@pytest.mark.password_manager
def test_generate_hash(fake_password, fake_hash):
    hashed = PasswordManager.generate_hash(fake_password)

    actual_type, actual_algorithm, _ = hashed.split(":")

    expected_type, expected_algorithm, _ = fake_hash.split(":")

    # Проверяем возвращаемый тип
    assert isinstance(hashed, str)

    # Проверяем длину хэша
    assert len(hashed) > 0

    # Сравниваем два первых сегмента хэша
    assert actual_type == expected_type
    assert actual_algorithm == expected_algorithm


@pytest.mark.password_manager
def test_check_hash(fake_password, fake_hash):
    result = PasswordManager.check_hash(fake_hash, fake_password)

    # Проверяем возвращаемый тип
    assert isinstance(result, bool)

    # Проверяем возвращаемое значение
    assert result is True
