from pydantic import BaseModel


class AuthTokens(BaseModel):
    access: str
    refresh: str
