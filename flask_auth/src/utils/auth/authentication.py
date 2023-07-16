import uuid
from abc import ABC, abstractmethod
from typing import Type

from core.config import BaseRoles
from db.cache import Redis
from models.models_pydantic import AuthRequest, Payload
from utils.auth.utils import AuthenticationManager, RequestParser


class BaseAuthentication(ABC):
    @abstractmethod
    def authenticate(self) -> AuthRequest:
        pass

    @abstractmethod
    def get_user_id(self) -> uuid.UUID | None:
        pass

    @abstractmethod
    def issue_token_pair(self) -> dict[str, str] | None:
        pass


class Authentication(BaseAuthentication):
    def __init__(self, request: dict, request_parser: Type[RequestParser] = RequestParser,
                 cache=Redis) -> None:
        self.request = request
        self.request_parser = request_parser(request)
        self.payload: Payload | bool | None = None
        self.cache: Redis = Redis(cache)

    def authenticate(self) -> AuthRequest:
        """
        Defines user authentication, their roles, and what they want.
        """
        if self.payload is None:
            self.payload = self.request_parser.get_payload_if_token_correct()
        # print(self.payload)
        authrequest = self.request_parser.get_auth_request(self.payload)
        if authrequest.roles == [BaseRoles.ANONIMOUS.value]:
            self.payload = False

        if self.payload:
            AuthenticationManager.save_history(self.request, self.payload)
        return authrequest

    def get_user_id(self) -> uuid.UUID | None:
        """
        Get user_id from payload.
        """
        if self.payload is None:
            self.payload = self.request_parser.get_payload_if_token_correct()
        if type(self.payload) == Payload:
            return self.payload.user_id
        return None

    def issue_token_pair(self) -> dict[str, str] | None:
        """
        Generate a new pair of tokens.
        """
        fingerprint = self.request_parser.get_fingerprint()
        if self.payload is None:
            self.payload = self.request_parser.get_payload_if_token_correct()
            if type(self.payload) == Payload:
                return AuthenticationManager.issue_token_pair(self.payload, self.request,
                                                              fingerprint, self.cache)
            return None
        elif type(self.payload) == Payload:
            return AuthenticationManager.issue_token_pair(self.payload, self.request,
                                                          fingerprint, self.cache)
        return None
