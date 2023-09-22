from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str


class UserResponse(BaseModel):
    username: str
    surname: str
    email: str
    eth_address: Optional[str]


class TokenData(BaseModel):
    username: str = None
