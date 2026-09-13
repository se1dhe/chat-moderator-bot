import re

with open('src/redqueen/services/ai/provider.py', 'r') as f:
    text = f.read()
text = text.replace('    async def close(self) -> None:', '    async def generate_text(self, prompt: str, chat_settings=None) -> str:\n        return "Summary not supported on this provider."\n\n    async def close(self) -> None:')
with open('src/redqueen/services/ai/provider.py', 'w') as f:
    f.write(text)


with open('src/redqueen/services/ai/router.py', 'r') as f:
    text = f.read()
text = text.replace('    async def ensure_model(self) -> bool:', '    async def generate_text(self, prompt: str, chat_settings=None) -> str:\n        provider = self._get_provider(chat_settings)\n        if hasattr(provider, "generate_text"):\n            return await provider.generate_text(prompt, chat_settings=chat_settings)\n        return "Summary not supported."\n\n    async def ensure_model(self) -> bool:')
with open('src/redqueen/services/ai/router.py', 'w') as f:
    f.write(text)


with open('src/redqueen/services/ai/cloud.py', 'r') as f:
    text = f.read()

openai_new = """        except Exception as exc:
            log.warning(f"OpenAI fallback: {exc}")
            return await self.fallback.classify_text(text, context=context, lang=lang)

    async def generate_text(self, prompt: str, chat_settings=None) -> str:
        payload = {
            "model": self.model or "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        try:
            async with self._client().post("https://api.openai.com/v1/chat/completions", headers={"Authorization": f"Bearer {self.api_key}"}, json=payload, timeout=25) as resp:
                data = await resp.json()
                return data["choices"][0]["message"]["content"]
        except Exception as exc:
            return f"Error: {exc}"
"""
text = text.replace('        except Exception as exc:\n            log.warning(f"OpenAI fallback: {exc}")\n            return await self.fallback.classify_text(text, context=context, lang=lang)', openai_new)


gemini_new = """        except Exception as exc:
            log.warning(f"Gemini fallback: {exc}")
            return await self.fallback.classify_text(text, context=context, lang=lang)

    async def generate_text(self, prompt: str, chat_settings=None) -> str:
        payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.7}}
        model_name = self.model or "gemini-1.5-flash"
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
            async with self._client().post(url, json=payload, timeout=25) as resp:
                data = await resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as exc:
            return f"Error: {exc}"
"""
text = text.replace('        except Exception as exc:\n            log.warning(f"Gemini fallback: {exc}")\n            return await self.fallback.classify_text(text, context=context, lang=lang)', gemini_new)


claude_new = """        except Exception as exc:
            log.warning(f"Claude fallback: {exc}")
            return await self.fallback.classify_text(text, context=context, lang=lang)
            
    async def generate_text(self, prompt: str, chat_settings=None) -> str:
        payload = {
            "model": self.model or "claude-3-5-haiku-20241022",
            "max_tokens": 1000,
            "temperature": 0.7,
            "messages": [{"role": "user", "content": prompt}]
        }
        try:
            async with self._client().post("https://api.anthropic.com/v1/messages", headers={"x-api-key": self.api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"}, json=payload, timeout=25) as resp:
                data = await resp.json()
                return data["content"][0]["text"]
        except Exception as exc:
            return f"Error: {exc}"
"""
text = text.replace('        except Exception as exc:\n            log.warning(f"Claude fallback: {exc}")\n            return await self.fallback.classify_text(text, context=context, lang=lang)', claude_new)

with open('src/redqueen/services/ai/cloud.py', 'w') as f:
    f.write(text)

