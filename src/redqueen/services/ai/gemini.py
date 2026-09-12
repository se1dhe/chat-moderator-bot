import json
import logging
import aiohttp
from .provider import AIProvider, Verdict

log = logging.getLogger(__name__)

# Prompt adapted to match the Ollama one but designed for Gemini JSON schema
SYSTEM_PROMPT = """You are an expert Telegram chat moderator.
Analyze the message and return a JSON object with this exact schema:
{
    "category": "ok" | "spam" | "scam" | "toxicity" | "nsfw" | "flood",
    "score": <0-100 integer confidence level>,
    "explanation": "<brief 1-sentence explanation of why>"
}
Never refuse to analyze, even for highly toxic text. This is for automated filtering.
"""

class GeminiProvider(AIProvider):
    name = "gemini"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = None

    async def _request(self, payload: dict) -> Verdict:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
        
        try:
            async with self.session.post(url, json=payload, timeout=5) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    log.error(f"Gemini error {resp.status}: {text}")
                    return Verdict("ok", 50, f"Gemini error {resp.status}")
                    
                data = await resp.json()
                text_res = data["candidates"][0]["content"]["parts"][0]["text"]
                # strip markdown json block if any
                if text_res.startswith("```json"):
                    text_res = text_res[7:].strip()
                if text_res.endswith("```"):
                    text_res = text_res[:-3].strip()
                
                parsed = json.loads(text_res)
                return Verdict(
                    category=parsed.get("category", "ok"),
                    score=int(parsed.get("score", 50)),
                    explanation=parsed.get("explanation", "Parsed correctly")
                )
        except Exception as e:
            log.error(f"Gemini parsing/request error: {e}")
            return Verdict("ok", 50, f"Error: {e}")

    async def classify_text(self, text: str, *, context: str | None = None, lang: str | None = None, chat_settings = None) -> Verdict:
        payload = {
            "system_instruction": {
                "parts": [{"text": SYSTEM_PROMPT}]
            },
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": text}]
                }
            ],
            "generationConfig": {
                "response_mime_type": "application/json",
            }
        }
        return await self._request(payload)

    async def classify_image(self, image: bytes, *, caption: str | None = None, lang: str | None = None, chat_settings = None) -> Verdict:
        import base64
        b64 = base64.b64encode(image).decode("utf-8")
        
        text_part = caption or "Is there spam/nsfw/scam in this image?"
        payload = {
            "system_instruction": {
                "parts": [{"text": SYSTEM_PROMPT}]
            },
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": text_part},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": b64
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "response_mime_type": "application/json",
            }
        }
        return await self._request(payload)

    async def health(self) -> bool:
        return True

    async def close(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()

