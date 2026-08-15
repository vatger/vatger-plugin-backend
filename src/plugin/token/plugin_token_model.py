import uuid
from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class PluginTokenModel(SQLModel, table=True):
    __tablename__ = "plugin-tokens"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user: uuid.UUID | None = None
    label: str | None = None
    polling_secret: str | None = None
    token: str = Field(unique=True, index=True)
    last_used: datetime = Field(default_factory=lambda: datetime.now(UTC))
