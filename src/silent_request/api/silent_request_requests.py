from typing import Literal

from pydantic import BaseModel


class SilentRequestCreateRequest(BaseModel):
    type: Literal["TAXI", "PUSHBACK"]
