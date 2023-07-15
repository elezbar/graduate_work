import uuid
from datetime import datetime
from typing import Any, Callable, Optional

import orjson
from pydantic import BaseModel

from core.config import CRUD, TokenType


def orjson_dumps(v: Any, *, default: Optional[Callable[[Any], Any]]) -> str:
    return orjson.dumps(v, default=default).decode()


class ConfigMixin(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class User(ConfigMixin):
    id: uuid.UUID
    username: str
    password: str


class UserRole(ConfigMixin):
    id: uuid.UUID
    user_id: uuid.UUID
    role_id: uuid.UUID


class Role(ConfigMixin):
    id: uuid.UUID
    name: str


class AuthHistory(ConfigMixin):
    id: int | None
    user_id: uuid.UUID
    device: str
    datetime: datetime
    endpoint: str


class Permission(ConfigMixin):
    permission_object: uuid.UUID
    role_id: uuid.UUID
    permitted_action: CRUD
    object_id: uuid.UUID | None


class PermissionObject(ConfigMixin):
    id: uuid.UUID
    name: str


class Payload(ConfigMixin):
    user_id: uuid.UUID | None
    roles: list[uuid.UUID]
    iat: datetime | None
    exp: datetime | None
    token_type: TokenType | None

    def get_roles_str(self) -> list[str]:
        return list(map(str, self.roles))


class AuthRequest(ConfigMixin):
    action: CRUD
    roles: list[uuid.UUID]
    resource_types: list[PermissionObject | None]
    resource_id: uuid.UUID | int | None
    is_anonim: bool

    def get_roles_str(self) -> list[str]:
        return list(map(str, self.roles))
