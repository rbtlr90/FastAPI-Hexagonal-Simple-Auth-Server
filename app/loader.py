from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
import aioredis
import socketio

from app.config.redis import RedisSettings
from app.config.postgres import DatabaseSettings

database_settings = DatabaseSettings()
redis_settings = RedisSettings()


engine = create_async_engine(
    f'postgresql+asyncpg://{database_settings.db_user}:{database_settings.db_password}@{database_settings.db_address}:{database_settings.db_port}/{database_settings.database}',    # pylint: disable=C0301
    future=True,
    echo=True
)

Base = declarative_base()

async def get_session() -> AsyncSession:
    "Get async session"
    sess = AsyncSession(bind=engine, expire_on_commit=False)
    try:
        yield sess
    finally:
        await sess.close()

def get_redis_conn() -> aioredis.Redis:
    return aioredis.Redis.from_url(
        f"redis://{redis_settings.host}", encoding="utf-8", decode_responses=True
    )

redis_conn = get_redis_conn()

sio = socketio.AsyncServer(
        async_mode="asgi",
        cors_allowed_origins='*'
)

asgi_app = socketio.ASGIApp(
        socketio_server=sio,
        socketio_path='socket.io'
)
