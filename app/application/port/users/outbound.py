from typing import Protocol, List, runtime_checkable, Optional

from app.adapter.api.users.requests import UserCreateRequest
from app.adapter.persistence.users.schema import UserSchema
from app.domain.users.entity import User


@runtime_checkable
class AbstractUserRepository(Protocol):
    """ Python doesn't have interface keyword, 
        so implement interface class
        through duck-typing 
    """
    async def create_one_user(self, user_info: UserCreateRequest) -> Optional[User]:
        ...

    async def get_one_user_by_user_id(self, user_id: str) -> Optional[User]:
        ...

    async def get_user_list_paging(self, offset: int, limit: int, order: str) -> List[Optional[User]]:
        ...

    # async def set_session_id_to_user(self, user_id: str, session_id: str) -> bool:
    #     ...

    # async def unset_session_id_from_user(self, user_id: str, session_id: str) -> bool:
    #     ...
