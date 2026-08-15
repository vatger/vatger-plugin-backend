import uuid
from abc import ABC, abstractmethod

from silent_request.silent_request import SilentRequest
from users.user import User


class UserOfflineException(Exception): ...


class ControllerOfflineException(Exception): ...


class UserHasNoFlightplanException(Exception): ...


class UserMustBeControllerException(Exception): ...


class ExistingRequestException(Exception): ...


class NoExistingRequestException(Exception): ...


class InvalidAirportExpection(Exception): ...


class SilentRequestServiceInterface(ABC):
    @abstractmethod
    def get_requests_by_icao(self, icao: str) -> list[SilentRequest]: ...

    @abstractmethod
    def get_request_by_user(self, user_id: uuid.UUID) -> SilentRequest | None: ...

    @abstractmethod
    def get_all_requests(self) -> list[SilentRequest]: ...

    @abstractmethod
    async def create_request(self, user: User): ...

    @abstractmethod
    async def delete_request(self, actor: User, target_callsign: str | None = None) -> bool: ...
