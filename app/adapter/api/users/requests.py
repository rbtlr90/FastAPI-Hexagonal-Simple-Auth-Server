from typing import Optional

from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    user_id: str
    email_address: str
    password: str
    role: Optional[str]


class UserListQuery(BaseModel):
    offset: int
    limit: int
    order: str