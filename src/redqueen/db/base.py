"""SQLAlchemy async engine and session factory."""
from __future__ import annotations

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Declarative base for all models."""


_engine: AsyncEngine | None = None
_sessionmaker: async_sessionmaker[AsyncSession] | None = None


def init_engine(dsn: str, echo: bool = False) -> AsyncEngine:
    global _engine, _sessionmaker
    _engine = create_async_engine(dsn, echo=echo, pool_pre_ping=True)
    _sessionmaker = async_sessionmaker(_engine, expire_on_commit=False)
    return _engine


def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    if _sessionmaker is None:
        raise RuntimeError("Engine is not initialised. Call init_engine() first.")
    return _sessionmaker


async def create_all() -> None:
    """Dev bootstrap: create tables from metadata (use Alembic in prod)."""
    if _engine is None:
        raise RuntimeError("Engine is not initialised.")
    # Import models so they register on Base.metadata.
    from . import models  # noqa: F401

    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def dispose_engine() -> None:
    if _engine is not None:
        await _engine.dispose()
