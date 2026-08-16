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
    "You are RedQueen, a precise chat-moderation classifier for a multilingual "
    "(English/Russian/Ukrainian) Telegram community. Classify the LAST user message "
    "into exactly one category: ok, spam, scam, toxicity, nsfw, flood.\n"
    "Guidance:\n"
    "- scam: crypto/giveaway/investment lures, 'earn $X/day', paid-DM bait, phishing "
    "or invite links to external channels for profit.\n"
    "- spam: unsolicited ads, repeated promos, link dumps.\n"
    "- toxicity: insults, harassment, hate directed at people.\n"
    "- nsfw: sexual or explicit content.\n"
    "- flood: content-free noise, char spam, repetition.\n"
    "- ok: normal conversation, jokes, criticism of ideas (not people).\n"
    "Judge meaning across languages; do not flag a message merely for being non-English. "
    "Use the provided context only to disambiguate. Be calibrated: reserve scores above "
    "85 for clear violations.\n"
    "Return ONLY compact JSON: {\"category\": string, \"score\": integer 0-100, "
    "\"explanation\": short reason <= 20 words}. No prose."
)

# A couple of few-shot exchanges to anchor calibration and the JSON shape.
_FEWSHOT = [
    {"role": "user", "content": "Message: \"🚀 Free crypto airdrop! join t.me/xdrop and 10x your ETH today\""},
    {"role": "assistant", "content": '{"category": "scam", "score": 93, "explanation": "Crypto giveaway lure with external invite link"}'},
    {"role": "user", "content": "Message: \"доброе утро всем, как дела?\""},
    {"role": "assistant", "content": '{"category": "ok", "score": 96, "explanation": "Normal friendly greeting"}'},
    {"role": "user", "content": "Message: \"ты тупой идиот и ничего не понимаешь\""},
    {"role": "assistant", "content": '{"category": "toxicity", "score": 88, "explanation": "Direct personal insult"}'},
]


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

    async def model_available(self) -> bool:
        """Whether `self.model` is already downloaded on the Ollama host."""
        try:
            client = await self._client()
            async with client.get(f"{self.base_url}/api/tags", timeout=10) as resp:
                if resp.status != 200:
                    return False
                data = await resp.json()
        except Exception:  # noqa: BLE001
            return False
        names = {m.get("name", "") for m in data.get("models", [])}
        return self.model in names or f"{self.model}:latest" in names

    async def ensure_model(self) -> bool:
        """Pull `self.model` if it isn't present yet. Safe to call at startup; streams
        progress to the log. Returns True once the model is available."""
        try:
            if await self.model_available():
                log.info("Ollama model %s already present", self.model)
                return True
            log.info("Pulling Ollama model %s (this can take a while)…", self.model)
            client = await self._client()
            timeout = aiohttp.ClientTimeout(total=None, sock_read=None)
            async with client.post(
                f"{self.base_url}/api/pull",
                json={"model": self.model, "stream": True},
                timeout=timeout,
            ) as resp:
                resp.raise_for_status()
                last_status = None
                async for raw in resp.content:
                    line = raw.strip()
                    if not line:
                        continue
                    try:
                        msg = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if msg.get("error"):
                        log.error("Ollama pull failed for %s: %s — check OLLAMA_MODEL is a "
                                  "valid tag in the Ollama library", self.model, msg["error"])
                        return False
                    status = msg.get("status")
                    if status and status != last_status:
                        log.info("Ollama pull [%s]: %s", self.model, status)
                        last_status = status
            ok = await self.model_available()
            log.info("Ollama model %s ready: %s", self.model, ok)
            return ok
        except Exception as exc:  # noqa: BLE001
            log.warning("Ollama ensure_model failed (%s); AI stays on the rule fallback "
                        "until the model is available", exc)
            return False

    async def classify_text(
        self, text: str, *, context: str | None = None, lang: str | None = None
    ) -> Verdict:
        parts = []
        if lang:
            parts.append(f"Chat language: {lang}.")
        if context:
            parts.append(f"Context (message being replied to): \"{context[:500]}\"")
        parts.append(f"Message: \"{text[:4000]}\"")
        user_content = "\n".join(parts)

        payload = {
            "model": self.model,
            "format": "json",
            "stream": False,
            "options": {"temperature": 0},
            "messages": [
                {"role": "system", "content": _SYSTEM_PROMPT},
                *_FEWSHOT,
                {"role": "user", "content": user_content},
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
            return await self.fallback.classify_text(text, context=context, lang=lang)

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
