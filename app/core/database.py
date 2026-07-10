from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import setting

engine = create_async_engine(
    setting.DATABASE_URL,
    echo = setting.DEBUG,
    pool_size = 10,
    max_overflow = 20
)

AsyncSessionLocal = async_sessionmaker(engine,expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncSession:
    
    async with AsyncSessionLocal():
        try:
            yield AsyncSessionLocal()
            await AsyncSessionLocal.commit()
        except Exception:
            await session.rollback()
            raise
