"""Shared pytest fixtures."""
from __future__ import annotations

import pytest


class FakeRedis:
    """Minimal in-memory stand-in for the handful of redis.asyncio calls M2 uses."""

    def __init__(self) -> None:
        self._values: dict[str, str] = {}
        self._sets: dict[str, set[str]] = {}

    async def incr(self, key: str) -> int:
        current = int(self._values.get(key, "0")) + 1
        self._values[key] = str(current)
        return current

    async def expire(self, key: str, seconds: int) -> None:
        return None

    async def set(self, key: str, value: str, *, nx: bool = False, ex: int | None = None) -> bool:
        if nx and key in self._values:
            return False
        self._values[key] = value
        return True

    async def get(self, key: str) -> str | None:
        return self._values.get(key)

    async def smembers(self, key: str) -> set[str]:
        return self._sets.get(key, set())

    async def sadd(self, key: str, *values: str) -> None:
        self._sets.setdefault(key, set()).update(values)


@pytest.fixture
def fake_redis() -> FakeRedis:
    return FakeRedis()
