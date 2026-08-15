import uuid
from datetime import datetime
from enum import StrEnum

from sqlmodel import Field, SQLModel


class SilentRequestType(StrEnum):
    TAXI = "TAXI"
    PUSHBACK = "PUSHBACK"


class SilentRequestModel(SQLModel, table=True):
    __tablename__ = "silent-requests"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    callsign: str = Field(unique=True, index=True)
    user_id: uuid.UUID = Field(unique=True, index=True)
    departure_icao: str
    type: SilentRequestType
    requested_at: datetime
