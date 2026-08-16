from pydantic import BaseModel


class UserInfoResponse(BaseModel):
    cid: str
    name: str
    rating: str
    access: bool = False
    admin: bool = False
