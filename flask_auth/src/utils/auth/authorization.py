from abc import ABCMeta, abstractmethod

from core.config import BaseRoles
from models.models_pydantic import AuthRequest
from utils.auth.utils import AuthorizationManager


class BaseAuthorization(metaclass=ABCMeta):
    @abstractmethod
    def is_authorise(self) -> bool:
        pass


class Authorization(BaseAuthorization):
    def __init__(self, request: AuthRequest) -> None:
        self.request = request

    def is_authorise(self) -> bool:
        """
        Returns bool resolution by analyzing incoming data.
        """
        if BaseRoles.SUPERUSER.value in self.request.get_roles_str():
            return True
        auth_manager = AuthorizationManager(self.request)
        cache_result = auth_manager.check_in_cache()
        if cache_result is not None:
            return cache_result
        elif auth_manager.check_in_db():
            auth_manager.save_to_cache(True)
            return True
        auth_manager.save_to_cache(False)
        return False
