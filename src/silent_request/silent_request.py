import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class SilentRequest(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    callsign: str
    user_id: uuid.UUID
    departure_icao: str
    type: Literal["TAXI", "PUSHBACK"]
    requested_at: datetime
