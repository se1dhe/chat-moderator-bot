"""Cloud AI Providers (OpenAI, Gemini, Claude)."""
import json
import logging
import aiohttp
from .provider import CATEGORIES, AIProvider, Verdict

log = logging.getLogger(__name__)

_SYSTEM_PROMPT = (
    "You are RedQueen, a chat-moderation classifier. "
    "Classify the LAST user message into exactly one category: ok, spam, scam, toxicity, nsfw, flood.\n"
    "Return ONLY compact JSON: {\"category\": string, \"score\": integer 0-100, "
    "\"explanation\": short reason <= 20 words}. No prose."
)

class CloudAIProvider(AIProvider):
    def __init__(self, api_key: str, model: str, fallback: AIProvider):
        self.api_key = api_key
        self.model = model
        self.fallback = fallback
        self._session: aiohttp.ClientSession | None = None

    def _client(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

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

class OpenAIProvider(CloudAIProvider):
    name = "openai"

    async def classify_text(self, text: str, *, context: str | None = None, lang: str | None = None, chat_settings=None) -> Verdict:
        parts = []
        if lang:
            parts.append(f"Chat language: {lang}.")
        if context:
            parts.append(f"Context: \"{context[:500]}\"")
        parts.append(f"Message: \"{text[:4000]}\"")
        
        payload = {
            "model": self.model or "gpt-4o-mini",
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": "\n".join(parts)}
            ],
            "temperature": 0.0
        }
        try:
            async with self._client().post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=payload,
                timeout=15
            ) as resp:
                if resp.status != 200:
                    log.warning(f"OpenAI error: {await resp.text()}")
                    return await self.fallback.classify_text(text, context=context, lang=lang)
                data = await resp.json()
                content = data["choices"][0]["message"]["content"]
                return self._to_verdict(json.loads(content))
        except Exception as exc:
            log.warning(f"OpenAI fallback: {exc}")
            return await self.fallback.classify_text(text, context=context, lang=lang)

class GeminiProvider(CloudAIProvider):
    name = "gemini"

    async def classify_text(self, text: str, *, context: str | None = None, lang: str | None = None, chat_settings=None) -> Verdict:
        parts = [_SYSTEM_PROMPT]
        if lang:
            parts.append(f"Chat language: {lang}.")
        if context:
            parts.append(f"Context: \"{context[:500]}\"")
        parts.append(f"Message: \"{text[:4000]}\"")
        
        model_name = self.model or "gemini-1.5-flash"
        payload = {
            "contents": [{"parts": [{"text": "\n".join(parts)}]}],
            "generationConfig": {
                "temperature": 0.0,
                "responseMimeType": "application/json",
            }
        }
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
            async with self._client().post(url, json=payload, timeout=15) as resp:
                if resp.status != 200:
                    log.warning(f"Gemini error: {await resp.text()}")
                    return await self.fallback.classify_text(text, context=context, lang=lang)
                data = await resp.json()
                content = data["candidates"][0]["content"]["parts"][0]["text"]
                return self._to_verdict(json.loads(content))
        except Exception as exc:
            log.warning(f"Gemini fallback: {exc}")
            return await self.fallback.classify_text(text, context=context, lang=lang)

class ClaudeProvider(CloudAIProvider):
    name = "claude"

    async def classify_text(self, text: str, *, context: str | None = None, lang: str | None = None, chat_settings=None) -> Verdict:
        parts = []
        if lang:
            parts.append(f"Chat language: {lang}.")
        if context:
            parts.append(f"Context: \"{context[:500]}\"")
        parts.append(f"Message: \"{text[:4000]}\"")
        
        payload = {
            "model": self.model or "claude-3-5-haiku-20241022",
            "max_tokens": 300,
            "temperature": 0.0,
            "system": _SYSTEM_PROMPT,
            "messages": [
                {"role": "user", "content": "\n".join(parts)}
            ]
        }
        try:
            async with self._client().post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                },
                json=payload,
                timeout=15
            ) as resp:
                if resp.status != 200:
                    log.warning(f"Claude error: {await resp.text()}")
                    return await self.fallback.classify_text(text, context=context, lang=lang)
                data = await resp.json()
                content = data["content"][0]["text"]
                return self._to_verdict(json.loads(content))
        except Exception as exc:
            log.warning(f"Claude fallback: {exc}")
            return await self.fallback.classify_text(text, context=context, lang=lang)
