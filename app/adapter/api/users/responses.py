from typing import List, Optional

from pydantic import BaseModel


class UserCreateResponse(BaseModel):
    user_id: str
    email_address: str
    role: str


class UserListResponse(BaseModel):
    users: List[Optional[UserCreateResponse]]
