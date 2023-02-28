import os

from pydantic import BaseSettings


class DatabaseSettings(BaseSettings):
    database: str = os.getenv("DATABASE", "simple_postgres")
    db_address: str = os.getenv("DB_ADDRESS", "127.0.0.1")
    db_user: str = os.getenv("DB_USER", "auth_user")
    db_password: str = os.getenv("DB_PASSWORD", "qwer1234")
    db_port: int = int(os.getenv("DB_PORT", "5432"))
