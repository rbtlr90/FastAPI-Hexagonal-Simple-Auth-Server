import datetime

from sqlalchemy import Column, Integer, String, DateTime

from app.loader import Base
from app.domain.users.entity import User


class UserSchema(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(20), nullable=False, unique=True)
    email_address = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def to_domain(self) -> User:
        return User(
            self.id,
            self.user_id,
            self.email_address,
            self.password,
            self.role,
            self.created_at,
            self.updated_at
        )

    @staticmethod
    def from_domain(user: User) -> "UserSchema":
        return UserSchema(
            user.id,
            user.user_id,
            user.email_address,
            user.password,
            user.role,
            user.created_at,
            user.updated_at
        )
