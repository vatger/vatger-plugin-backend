import uuid

from sqlmodel import Field, SQLModel


class UserModel(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    cid: str = Field(unique=True, index=True)
    name: str
    rating: str
    admin: bool = False
    access: bool = False
