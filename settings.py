import os

import dotenv
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from redis.asyncio import Redis


dotenv.load_dotenv()


class DatabaseConfig:
    DATABASE_NAME = os.getenv("DATABASE_NAME", "async_db")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    SECRET_KEY = os.getenv("SECRET_KEY")

    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

    def redis_client(self) -> Redis:
        return Redis(
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            db=self.REDIS_DB,
            password=self.REDIS_PASSWORD,
            decode_responses=True,
        )

    def uri_postgres(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@localhost:5432/{self.DATABASE_NAME}"

    def uri_sqlite(self):
        return f"sqlite+aiosqlite:///{self.DATABASE_NAME}.db"

    def uri_mysql(self):
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@localhost/{self.DATABASE_NAME}"


api_config = DatabaseConfig()


# Налаштування бази даних Postgres
# engine = create_engine(api_config.uri_postgres(), echo=True)
async_engine: AsyncEngine = create_async_engine(api_config.uri_sqlite(), echo=True)
async_session = async_sessionmaker(bind=async_engine)


# Декларація базового класу для моделей, Необхідно для реалізації відношень у ORM
class Base(AsyncAttrs, DeclarativeBase):
    pass


# Dependency: сесія БД для FastAPI
async def get_db():
    async with async_session() as session:
        yield session
