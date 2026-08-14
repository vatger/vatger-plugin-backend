import uuid
from abc import ABC, abstractmethod

from users.user import User


class UserAlreadyExistsError(Exception):
    def __init__(self, cid: int):
        super().__init__(f"User with cid {cid} already exists")
        self.cid = cid


class UserRepositoryInterface(ABC):
    @abstractmethod
    def get_user(self, id: uuid.UUID) -> User: ...

    @abstractmethod
    def get_user_by_cid(self, cid: str) -> User: ...

    @abstractmethod
    def add_user(self, user: User): ...

    @abstractmethod
    def update_user(self, user: User): ...
