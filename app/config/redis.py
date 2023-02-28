import os

from pydantic import BaseSettings


class RedisSettings(BaseSettings):
    host: str = os.getenv("REDIS_HOST", "localhost")
    port: str = os.getenv("REDIS_PORT", "6379")
    db: str = os.getenv("REDIS_DB", "0")
    socket_timeout: int = int(os.getenv("REDIS_SOCKET_TIMEOUT", "5"))
