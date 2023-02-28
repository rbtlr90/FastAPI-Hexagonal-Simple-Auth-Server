from typing import Protocol, runtime_checkable, Optional
from datetime import timedelta

from app.domain.users.entity import User
from app.adapter.api.auth.responses import Token


@runtime_checkable
class AbstractTokenUsecase(Protocol):
    """ Python doesn't have interface keyword, 
        so implement interface class
        through duck-typing 
    """
    def create_token(self, user: User, token_type: str, 
                            expires_delta: Optional[timedelta] = None) -> Token:
        ...

    def validate_token(self, token: str) -> bool:
        ...

    def get_id_from_token(self, token: str) -> str:
        ...

    def get_role_from_token(self, token: str) -> str:
        ...

    def get_token_type_from_token(cls, token: str) -> str:
        ...
