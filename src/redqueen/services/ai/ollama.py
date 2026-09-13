"""Ollama-backed provider using a local Qwen model.

Talks to the Ollama HTTP API (/api/chat) with JSON output format and asks the model
to return a strict moderation verdict. Any failure degrades to the rule fallback so
moderation never hard-depends on the model being up.
"""
from __future__ import annotations

import base64
import json
import logging

import aiohttp

from .provider import CATEGORIES, AIProvider, Verdict

log = logging.getLogger(__name__)

_VISION_PROMPT = (
    "You are RedQueen, a chat-moderation classifier inspecting an IMAGE shared in a "
    "community. Classify it into exactly one category: ok, spam, scam, toxicity, nsfw, "
    "flood. Focus on: crypto/giveaway/investment scam posters, phishing screenshots, "
    "QR-code lures, sexual/explicit (nsfw) content, gore/hate imagery (toxicity). "
    "Read any text in the image, across languages. Reserve scores above 85 for clear "
    "violations. Return ONLY compact JSON: {\"category\": string, \"score\": integer "
    "0-100, \"explanation\": short reason <= 20 words}. No prose."
)

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

    def __init__(
        self, base_url: str, model: str, fallback: AIProvider, vision_model: str = ""
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.vision_model = vision_model
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

    async def model_available(self, model: str | None = None) -> bool:
        """Whether `model` (default the text model) is downloaded on the Ollama host."""
        target = model or self.model
        try:
            client = await self._client()
            async with client.get(f"{self.base_url}/api/tags", timeout=10) as resp:
                if resp.status != 200:
                    return False
                data = await resp.json()
        except Exception:  # noqa: BLE001
            return False
        names = {m.get("name", "") for m in data.get("models", [])}
        return target in names or f"{target}:latest" in names

    async def _pull(self, model: str) -> bool:
        if await self.model_available(model):
            log.info("Ollama model %s already present", model)
            return True
        log.info("Pulling Ollama model %s (this can take a while)…", model)
        client = await self._client()
        timeout = aiohttp.ClientTimeout(total=None, sock_read=None)
        async with client.post(
            f"{self.base_url}/api/pull", json={"model": model, "stream": True}, timeout=timeout,
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
                    log.error("Ollama pull failed for %s: %s — check the model is a valid "
                              "tag in the Ollama library", model, msg["error"])
                    return False
                status = msg.get("status")
                if status and status != last_status:
                    log.info("Ollama pull [%s]: %s", model, status)
                    last_status = status
        ok = await self.model_available(model)
        log.info("Ollama model %s ready: %s", model, ok)
        return ok

    async def ensure_model(self) -> bool:
        """Pull the text model (and the vision model if configured) when missing.
        Safe to call at startup; degrades to the rule fallback on any failure."""
        try:
            ok = await self._pull(self.model)
            if self.vision_model:
                await self._pull(self.vision_model)
            return ok
        except Exception as exc:  # noqa: BLE001
            log.warning("Ollama ensure_model failed (%s); AI stays on the rule fallback "
                        "until the model is available", exc)
            return False

    async def classify_text(
        self, text: str, *, context: str | None = None, lang: str | None = None, chat_settings = None
    ) -> Verdict:
        parts = []
        if lang:
            parts.append(f"Chat language: {lang}.")
        if context:
            parts.append(f"Context (message being replied to): \"{context[:500]}\"")
        parts.append(f"\n---BEGIN USER MESSAGE---\n{text[:4000]}\n---END USER MESSAGE---\n")
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

    async def classify_image(
        self, image: bytes, *, caption: str | None = None, lang: str | None = None, chat_settings = None
    ) -> Verdict:
        if not self.vision_model:
            return await self.fallback.classify_image(image, caption=caption, lang=lang)
        user = f"Chat language: {lang}. " if lang else ""
        user += f'Caption: "{caption[:500]}"' if caption else "No caption."
        payload = {
            "model": self.vision_model,
            "format": "json",
            "stream": False,
            "options": {"temperature": 0},
            "messages": [
                {"role": "system", "content": _VISION_PROMPT},
                {"role": "user", "content": user, "images": [base64.b64encode(image).decode()]},
            ],
        }
        try:
            client = await self._client()
            async with client.post(
                f"{self.base_url}/api/chat", json=payload, timeout=60
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()
            return self._to_verdict(json.loads(data["message"]["content"]))
        except Exception as exc:  # noqa: BLE001
            log.warning("Ollama vision classify failed, using fallback: %s", exc)
            return await self.fallback.classify_image(image, caption=caption, lang=lang)

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
