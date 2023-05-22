from redis import Redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config import settings

engine = create_async_engine(settings.DB_URI)
SessionLocal = async_sessionmaker(bind=engine, autoflush=False, class_=AsyncSession)

def RedisSession():
    return Redis.from_url(url=settings.REDIS_URI, decode_responses=True)