import uuid
from abc import ABC, abstractmethod

from silent_request.silent_request import SilentRequest


class DuplicateSilentRequestException(Exception): ...


class SilentRequestRepositoryInterface(ABC):
    @abstractmethod
    def create_request(self, request: SilentRequest) -> SilentRequest: ...

    @abstractmethod
    def get_request_by_callsign(self, callsign: str) -> SilentRequest | None: ...

    @abstractmethod
    def get_request_by_user_id(self, id: uuid.UUID) -> SilentRequest | None: ...

    @abstractmethod
    def get_requests_by_icao(self, icao: str) -> list[SilentRequest] | None: ...

    @abstractmethod
    def get_all_requests(self) -> list[SilentRequest] | None: ...

    @abstractmethod
    def delete_request_by_callsign(self, callsign: str) -> bool: ...

    @abstractmethod
    def delete_request_by_user(self, user_id: uuid.UUID) -> bool: ...
