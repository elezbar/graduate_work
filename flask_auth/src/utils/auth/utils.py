import datetime as dt
import hashlib
import uuid
from abc import ABCMeta, abstractmethod
from typing import Any, Tuple

from flask import Request
from flask_restful import reqparse

from core.config import BaseRoles, config, CRUD, METHOD_TO_CRUD, TYPES_WITH_ID
from core.logger import get_logger
from db.alchemy import session
from db.cache import Redis, get_redis
from models.models import AuthHistory
from models.models import Permission as PermissionDB
from models.models import PermissionObject as PermissionObjectDB
from models.models_pydantic import AuthRequest, Payload, Permission, PermissionObject
from utils.token.service import TokenManager, TokenType

logger = get_logger(__name__)


class BaseRequestParser(metaclass=ABCMeta):
    @abstractmethod
    def get_payload_if_token_correct(self) -> Payload | bool | None:
        pass

    @abstractmethod
    def token_exists(self) -> bool:
        pass

    @abstractmethod
    def get_fingerprint(self) -> str:
        pass

    @abstractmethod
    def get_token(self) -> Payload | bool | None:
        pass

    @abstractmethod
    def get_user_roles(self, payload: Payload | bool | None) -> list[str]:
        pass

    @abstractmethod
    def get_item_types(self, session) -> list[PermissionObject | None]:
        pass

    @abstractmethod
    def get_action_type(self) -> CRUD:
        pass

    @abstractmethod
    def get_auth_request(self, payload: Payload | bool | None) -> AuthRequest:
        pass

    @abstractmethod
    def request_pre_parser(
        cls,
        request: Request | None,
        parser: reqparse.RequestParser,
        request_type: str,
        entrypoint: str,
        request_obj_types: list | None,
    ) -> Tuple[Any, Any]:
        pass


class RequestParser(BaseRequestParser):
    def __init__(self, request: dict) -> None:
        self.request = request
        self.payload: Payload | bool | None = None

    def get_payload_if_token_correct(self) -> Payload | bool | None:
        """
        Verifying relevance of token. Returns Payload.
        """
        try:
            if self.request["Authorization"]:
                self.payload = TokenManager.decode(self.request["Authorization"])
                return self.payload
            return None
        except Exception as e:
            logger.exception(e)
            return None

    def token_exists(self) -> bool:
        """
        Checking for the presence of token.
        """
        return bool(self.request["Authorization"])

    def get_fingerprint(self) -> str:
        """
        Generate hashed fingerprint from request headers.
        """
        user_agent = str(self.request["User-Agent"]).encode()
        md5 = hashlib.md5()
        md5.update(user_agent)
        fingerprint = md5.hexdigest()
        return fingerprint

    def get_token(self) -> Payload | bool | None:
        """
        Extracting token from request headers.
        """
        if self.request["Authorization"]:
            return TokenManager.base64_decode(self.request["Authorization"])
        return None

    def get_user_roles(self, payload: Payload | bool | None) -> list[str]:
        """
        Extracting user roles from Payload.
        """
        if type(payload) == Payload:
            return list(map(str, payload.roles))
        return [BaseRoles.ANONIMOUS.value]

    @session
    def get_item_types(self, session) -> list[PermissionObject | None]:
        """
        Extracting user roles from Payload.
        """
        obj_types = self.request["RequestedObjTypes"]
        objs = session.query(PermissionObjectDB).filter(PermissionObjectDB.name.in_(obj_types))
        objs = session.execute(objs)
        obj_types = []
        for obj in objs:
            obj_types.append(PermissionObject(**obj[0].serialize()))
        return obj_types

    def get_action_type(self) -> CRUD:
        """
        Convert request method to CRUD.
        """
        r_type = self.request["RequestType"]
        if r_type == "post":
            return CRUD.CREATE
        elif r_type in ["put", "patch"]:
            return CRUD.UPDATE
        elif r_type == "delete":
            return CRUD.DELETE
        return CRUD.READ

    def get_auth_request(self, payload: Payload | bool | None) -> AuthRequest:
        """
        Generate AuthRequest (what user want) from Payload.
        """
        return AuthRequest(
            action=self.get_action_type(),
            roles=self.get_user_roles(payload),
            resource_types=self.get_item_types(),
            resource_id=self.request["RequestedObjId"],
            is_anonim=not bool(payload),
        )

    @classmethod
    def request_pre_parser(
        cls,
        request: Request | None,
        parser: reqparse.RequestParser,
        request_type: str,
        entrypoint: str,
        request_obj_types: list | None,
    ) -> Tuple[Any, Any]:
        """
        Connects data from json and headers.
        """
        data = None
        if request:
            data = request.get_json(force=False, silent=True)
        args = parser.parse_args()
        args["RequestedObjId"] = None
        if data:
            if "RequestedObjTypes" in data:
                if data["RequestedObjTypes"]:
                    args["RequestedObjTypes"] = list(data["RequestedObjTypes"].split(", "))
            if "RequestedObjId" in data:
                if data["RequestedObjId"]:
                    args["RequestedObjId"] = data["RequestedObjId"]
            if "RequestType" in data:
                if data["RequestType"]:
                    args["RequestType"] = data["RequestType"]
        if request_obj_types:
            args["RequestedObjTypes"] = request_obj_types
        if request_type:
            args["RequestType"] = request_type
        args["Entrypoint"] = entrypoint
        return data, args


class BaseAuthenticationManager(metaclass=ABCMeta):
    @abstractmethod
    def issue_token_pair(cls, payload: Payload, request: dict, fingerprint: str,
                         cache: Redis) -> dict | None:
        pass

    @abstractmethod
    def check_token_fingerprint(cls, user_id: uuid.UUID, old_token: str,
                                fingerprint: str, cache: Redis) -> bool:
        pass

    @abstractmethod
    def save_refresh_token(cls, refresh: str, user_id: uuid.UUID, fingerprint: str,
                           cache: Redis) -> None:
        pass

    @staticmethod
    @abstractmethod
    def generate_history_entry(request: dict, payload: Payload | bool | None) -> AuthHistory:
        pass

    @abstractmethod
    def save_history(cls, request: dict, payload: Payload | bool | None,
                     session) -> None:
        pass


class AuthenticationManager(BaseAuthenticationManager):
    @classmethod
    def issue_token_pair(cls, payload: Payload, request: dict, fingerprint: str,
                         cache: Redis) -> dict | None:
        """
        Generate a new pair of tokens.
        """
        old_token = request["Authorization"]
        if cls.check_token_fingerprint(payload.user_id, old_token, fingerprint, cache):
            payload_dict = payload.dict()
            payload_dict["user_id"] = str(payload.user_id)
            payload_dict["roles"] = ", ".join(payload.get_roles_str())
            access = TokenManager(TokenType.ACCESS).encode(payload_dict)
            refresh = TokenManager(TokenType.REFRESH).encode(payload_dict)
            cls.save_refresh_token(refresh, payload.user_id, fingerprint, cache)
            return {"access": access, "refresh": refresh}
        return None

    @classmethod
    def check_token_fingerprint(cls, user_id: uuid.UUID | None, old_token: str, fingerprint: str,
                                cache: Redis) -> bool:
        """
        Check old refresh token not blockes.
        """
        users_cache = cache.get(str(user_id))
        print('users_cache', users_cache)
        if users_cache:
            if users_cache[fingerprint] == old_token:
                return True
        return False

    @classmethod
    def save_refresh_token(cls, refresh: str, user_id: uuid.UUID | None, fingerprint: str,
                           cache: Redis) -> None:
        """
        Associate refresh token with fingerprint and save pair to cache.
        """
        users_cache = cache.get(str(user_id))
        if not users_cache:
            cache.set(str(user_id), {fingerprint: refresh})
        else:
            users_cache[fingerprint] = refresh
            cache.set(str(user_id), users_cache)
        cache.expire(str(user_id))

    @staticmethod
    def generate_history_entry(request: dict, payload: Payload | bool | None) -> AuthHistory:
        """
        Generate history entry to save in DB.
        """
        if type(payload) == Payload:
            user_id = payload.user_id
        user_id = None
        return AuthHistory(
            id=uuid.uuid4(),
            action=METHOD_TO_CRUD[request["RequestType"]],
            user_id=user_id,
            device=request["User-Agent"],
            datetime=dt.datetime.now(dt.timezone.utc),
            endpoint=request["Entrypoint"],
        )

    @classmethod
    @session
    def save_history(cls, request: dict, payload: Payload | bool | None, session) -> None:
        """
        Save history entry to DB.
        """
        hist_entr = cls.generate_history_entry(request, payload)
        session.add(hist_entr)
        session.commit()


class BaseAuthorizationManager(metaclass=ABCMeta):
    @abstractmethod
    def check_in_cache(self) -> bool | None:
        pass

    @abstractmethod
    def save_to_cache(self, value) -> None:
        pass

    @abstractmethod
    def check_in_db(self) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def parse_permissions(request: AuthRequest) -> list[Permission]:
        pass

    @abstractmethod
    def cache_clean(cls, key: str, cache=get_redis) -> None:
        pass


class AuthorizationManager(BaseAuthorizationManager):
    @session
    def __init__(self, request: AuthRequest, session, cache=get_redis) -> None:
        self.request = request
        self.key = f"{config.cache.cache_prefix_to_find}{request.json()}"
        self.cache: Redis = Redis(cache())
        self.session = session

    def check_in_cache(self) -> bool | None:
        """
        Check permission in cache.
        """
        resp = self.cache.get(self.key)
        if resp:
            return bool(resp)
        return None

    def save_to_cache(self, value) -> None:
        """
        Save permission to cache and set expire by defauld.
        """
        self.cache.set(self.key, value)
        self.cache.expire(self.key)

    def check_in_db(self) -> bool:
        """
        Check permission in DB.
        """
        permissions = self.parse_permissions(self.request)
        for permission in permissions:
            if permission:
                query = self.session.query(PermissionDB).filter_by(
                    permission_object_id=permission.permission_object,
                    role_id=permission.role_id,
                    permitted_action=permission.permitted_action.value,
                    object_id=permission.object_id,
                )
                objs = self.session.execute(query).all()
                for obj in objs:
                    if obj[0]:
                        return obj[0]
        return False

    @staticmethod
    def parse_permissions(request: AuthRequest) -> list[Permission]:
        """
        Permissions parsing.
        """
        permissions = []
        resource_id: uuid.UUID | int | None = request.resource_id
        resource_types: list[PermissionObject | None] = request.resource_types
        permitted_action: CRUD = request.action
        for r_type in resource_types:
            if r_type:
                for role in request.roles:
                    permissions.append(
                        Permission(
                            permission_object=r_type.id,
                            role_id=role,
                            permitted_action=permitted_action,
                            object_id=None
                        )
                    )
                    types_with_id = [e.value for e in TYPES_WITH_ID]
                    if resource_id and r_type.name in types_with_id:
                        permissions.append(
                            Permission(
                                permission_object=r_type.id,
                                role_id=role,
                                permitted_action=permitted_action,
                                object_id=resource_id,
                            )
                        )
        return permissions

    @classmethod
    def cache_clean(cls, key: str, cache=get_redis) -> None:
        """
        Save history entry to DB.
        """
        try:
            cache = cache()
            for key in cache.scan_iter(match=f"{key}*"):
                cache.delete(key)
        except Exception as e:
            logger.error(f"Error while cleaning cache by pattern {key}: {e}")
