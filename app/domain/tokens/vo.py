import os
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError


class JWT:
    SECRET_KEY = os.getenv("SECRET_KEY", "MYSECRETKEY")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    def __init__(
        self, user, token_type, expires_delta: Optional[timedelta] = None
    ) -> None:
        to_encode = {"user_id": user.user_id}
        expire = JWT._extend_expire(token_type, expires_delta)
        self.jwt_token = jwt.encode(
            JWT._update_token_data(to_encode, expire, token_type, user.role),
            self.SECRET_KEY,
            algorithm=self.ALGORITHM,
        )

    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, JWT):
            return (
                self.get_current_user_id(self.jwt_token)
                == self.get_current_user_id(obj.jwt_token)
            ) and (
                self._get_current_token_expire_time(self.jwt_token)
                == self._get_current_token_expire_time(obj.jwt_token)
            )
        return False

    @classmethod
    def _extend_expire(cls, token_type, expires_delta):
        if expires_delta:
            return datetime.utcnow() + expires_delta

        if token_type == "access":
            return datetime.utcnow() + timedelta(minutes=60)
        return datetime.utcnow() + timedelta(days=1)

    @classmethod
    def _update_token_data(cls, to_encode, expire, token_type, role) -> dict:
        to_encode.update(
            {"exp": expire, "token_type": token_type, "role": role, "iss": "sample_auth_issuer"}
        )
        return to_encode

    def _get_current_token_expire_time(self, token: str) -> timedelta:
        payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
        expire_time: timedelta = payload.get("exp")
        return expire_time

    @classmethod
    def validate_token(cls, token: str) -> bool:
        try:
            jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            return True
        except JWTError:
            return False

    @classmethod
    def get_current_user_id(cls, token: str) -> str:
        payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
        user_id: str = payload.get("user_id")
        return user_id

    @classmethod
    def get_current_token_role(cls, token: str) -> str:
        payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
        role: str = payload.get("role")
        return role

    @classmethod
    def get_current_token_type(cls, token: str) -> str:
        payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
        role: str = payload.get("token_type")
        return role
