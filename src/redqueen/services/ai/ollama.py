"""Ollama-backed provider using a local Qwen model.

Talks to the Ollama HTTP API (/api/chat) with JSON output format and asks the model
to return a strict moderation verdict. Any failure degrades to the rule fallback so
moderation never hard-depends on the model being up.
"""
from __future__ import annotations

import json
import logging

import aiohttp

from .provider import CATEGORIES, AIProvider, Verdict

log = logging.getLogger(__name__)

_SYSTEM_PROMPT = (
    "You are RedQueen, a chat-moderation classifier. Classify the user message into "
    "exactly one category from this list: ok, spam, scam, toxicity, nsfw, flood. "
    "Return ONLY a compact JSON object with keys: category (string), score (integer "
    "0-100 confidence), explanation (short reason, max 20 words). No prose."
)


class OllamaProvider(AIProvider):
    name = "ollama"

    def __init__(self, base_url: str, model: str, fallback: AIProvider) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.fallback = fallback
        self._session: aiohttp.ClientSession | None = None

    async def _client(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def health(self) -> bool:
        try:
            client = await self._client()
            async with client.get(f"{self.base_url}/api/tags", timeout=5) as resp:
                return resp.status == 200
        except Exception as exc:  # noqa: BLE001
            log.warning("Ollama health check failed: %s", exc)
            return False

    async def classify_text(self, text: str, *, context: str | None = None) -> Verdict:
        payload = {
            "model": self.model,
            "format": "json",
            "stream": False,
            "options": {"temperature": 0},
            "messages": [
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": text[:4000]},
            ],
        }
        try:
            client = await self._client()
            async with client.post(
                f"{self.base_url}/api/chat", json=payload, timeout=30
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()
            content = data["message"]["content"]
            parsed = json.loads(content)
            return self._to_verdict(parsed)
        except Exception as exc:  # noqa: BLE001
            log.warning("Ollama classify failed, using fallback: %s", exc)
            return await self.fallback.classify_text(text, context=context)

    @staticmethod
    def _to_verdict(parsed: dict) -> Verdict:
        category = str(parsed.get("category", "ok")).lower().strip()
        if category not in CATEGORIES:
            category = "ok"
        try:
            score = max(0, min(100, int(parsed.get("score", 0))))
        except (TypeError, ValueError):
            score = 0
        explanation = str(parsed.get("explanation", "")).strip() or "No explanation"
        return Verdict(category=category, score=score, explanation=explanation)

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()
