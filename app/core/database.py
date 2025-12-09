from sqlalchemy import text  # noqa
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings
from app.models.base import Base

DATABASE_URL = settings.database_url

# Создание асинхронного движка
engine = create_async_engine(DATABASE_URL, echo=True)
# Создание фабрики сессий, до ручного коммита данные не применяются
async_session = async_sessionmaker(engine, expire_on_commit=False)


# Функция создания всех таблиц
async def init_db():
    async with engine.begin() as conn:
        # await conn.execute(text("DROP TABLE IF EXISTS alembic_version"))
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# Функция получения сессии, возвращает одну сессию
async def get_session():
    async with async_session() as session:
        yield session
