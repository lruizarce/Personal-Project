from typing import Annotated
from collections.abc import AsyncGenerator

from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlmodel import SQLModel

# Class to create an instance of our DB settings
class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

# Creates an instance of our DatabaseSettings class
settings = DatabaseSettings()
# Connection pool to PostgresSQL
# Reuses connections instead of opening/closing for each query
# Handles reconnection if DB restarts
engine = create_async_engine(settings.database_url, echo=False)
# Creates database sessions
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def create_db_and_tables():
    # opens a connection from the pool
    # start a transaction
    # autocommits when the block exits
    async with engine.begin() as conn:
        # SQLModel.metadata contains info about all your models tables
        # create_all generates CREATE TABLE SQL for each model
        # .run_sync wraps a sync function to run in async context
        await conn.run_sync(SQLModel.metadata.create_all)

# Dependency generator
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]