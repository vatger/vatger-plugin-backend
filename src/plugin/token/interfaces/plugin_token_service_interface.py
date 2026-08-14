from abc import ABC, abstractmethod
from typing import Literal

from models.user import User
from plugin.token.plugin_token import PluginToken


class PluginTokenServiceInterface(ABC):
    @abstractmethod
    def start_plugin_auth_flow() -> PluginToken: ...

    @abstractmethod
    def get_authorization_redirect(token_id: str, user_id: str, label: str) -> str: ...

    @abstractmethod
    def exchange_polling_secret_for_token(self, token_id: str, secret: str) -> str | None: ...

    @abstractmethod
    def get_tokens(scope: Literal["own", "all"], user: User): ...

    @abstractmethod
    def revoke_token(token_id: str, user: User): ...

    @abstractmethod
    def get_active_token_from_bearer(self, bearer_token: str) -> PluginToken: ...
