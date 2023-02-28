import os

from datetime import datetime
from typing import List

from passlib.context import CryptContext

ADMIN_ROLES : List[str] = ['admin', 'superuser']
PWD_CONTEXT_SCHEME = os.getenv('PWD_CONTEXT_SCHEME', 'bcrypt')


class User:  # pylint: disable=R0902
    PWD_CONTEXT = CryptContext(schemes=[PWD_CONTEXT_SCHEME], deprecated="auto")

    def __init__(  # pylint: disable=R0913
        self,
        id: int,  # pylint: disable=W0622
        user_id: str,
        email_address: str,
        password: str,
        role: str,
        created_at: datetime = None,
        updated_at: datetime = None
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.email_address = email_address
        self.password = password
        self.role = role
        if created_at is not None:
            self.created_at = created_at
        else:
            self.created_at = datetime.utcnow()
        if updated_at is not None:
            self.updated_at = updated_at
        else:
            self.updated_at = datetime.utcnow()

    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, User):
            return self.id == obj.id
        return False

    @classmethod
    def get_hashed_password(cls, password) -> str:
        return cls.PWD_CONTEXT.hash(password)

    def is_admin(self) -> bool:
        return self.role in ADMIN_ROLES  # pylint: disable=R1714

    def verify_password(self, plain_password, hashed_password) -> bool:
        return self.PWD_CONTEXT.verify(plain_password, hashed_password)
