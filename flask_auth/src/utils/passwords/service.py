from werkzeug.security import check_password_hash, generate_password_hash

from core.config import config


class PasswordManager:
    method = config.security.password.hash_method
    salt_length = config.security.password.salt_length

    @classmethod
    def generate_hash(cls, password: str) -> str:
        return generate_password_hash(password, cls.method, cls.salt_length)

    @staticmethod
    def check_hash(pwhash: str, password: str) -> bool:
        return check_password_hash(pwhash, password)


if __name__ == "__main__":
    passw = "testpassw"
    passw_hash = PasswordManager.generate_hash(password=passw)
    result = PasswordManager.check_hash(passw_hash, passw)

    print(result)
