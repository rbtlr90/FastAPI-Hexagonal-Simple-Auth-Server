from typing import Protocol, runtime_checkable, Optional, List

from app.domain.users.entity import User
from app.adapter.api.users.requests import UserCreateRequest


@runtime_checkable
class AbstractUserUsecase(Protocol):
    """ Python doesn't have interface keyword,
        so implement interface class
        through duck-typing
    """
    async def create_one_user(self, user_info: UserCreateRequest) -> Optional[User]:
        ...

    async def get_users_with_paging(self, offset: int, limit: int, order: str)\
                                                                        -> List[Optional[User]]:
        ...

    async def get_one_user_by_user_id(self, user_id: str) -> Optional[User]:
        ...
