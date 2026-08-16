"""Short-lived Redis cache of AI verdicts keyed by normalized message text.

Raids and copy-paste spam repeat the same text many times; caching the verdict means
the model classifies each distinct message once per window instead of every occurrence.
"""
from __future__ import annotations

import hashlib
import json
import re

from redis.asyncio import Redis

from .ai.provider import Verdict

_WS = re.compile(r"\s+")
_TTL = 600  # seconds


def _key(chat_id: int, text: str) -> str:
    norm = _WS.sub(" ", text.strip().lower())
    digest = hashlib.sha256(norm.encode()).hexdigest()[:32]
    return f"rq:aicache:{chat_id}:{digest}"


async def get(redis: Redis, chat_id: int, text: str) -> Verdict | None:
    raw = await redis.get(_key(chat_id, text))
    if not raw:
        return None
    try:
        d = json.loads(raw)
        return Verdict(category=d["category"], score=int(d["score"]), explanation=d["explanation"])
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        return None


async def put(redis: Redis, chat_id: int, text: str, verdict: Verdict) -> None:
    payload = json.dumps({
        "category": verdict.category, "score": verdict.score, "explanation": verdict.explanation,
    })
    await redis.set(_key(chat_id, text), payload, ex=_TTL)
