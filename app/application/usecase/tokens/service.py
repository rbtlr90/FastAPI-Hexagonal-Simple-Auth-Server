from typing import Optional, List
from datetime import timedelta

from app.application.port.tokens.inbound import AbstractTokenUsecase
from app.domain.users.entity import User
from app.adapter.api.auth.responses import Token
from app.domain.tokens.vo import JWT


class TokenUsecaseImpl(AbstractTokenUsecase):
    @classmethod
    def create_token(cls, user: User, token_type: str,
                        expires_delta: Optional[timedelta] = None) -> Token:
        return JWT(user, token_type, expires_delta).jwt_token

    @classmethod
    def validate_token(cls, token: str) -> bool:
        return JWT.validate_token(token)

    @classmethod
    def get_id_from_token(cls, token: str) -> str:
        return JWT.get_current_user_id(token)

    @classmethod
    def get_role_from_token(cls, token: str) -> str:
        return JWT.get_current_token_role(token)

    @classmethod
    def get_token_type_from_token(cls, token: str) -> str:
        return JWT.get_current_token_type(token)

    @classmethod
    def login(cls, user: User) -> List[str]:
        access_token = JWT(user, token_type="access").jwt_token
        refresh_token = JWT(user, token_type="refresh").jwt_token
        return [access_token, refresh_token]
