import re

with open('src/redqueen/handlers/ai_review.py', 'r') as f:
    text = f.read()

# Replace _classify_with_semaphore
old_func = """async def _classify_with_semaphore(sem, provider, text, context, lang, settings):
    async with sem:
        return await provider.classify_text(text, context=context, lang=lang, chat_settings=settings)"""

new_func = """async def _classify_with_semaphore(sem, provider, text, context, lang, settings):
    # Wait for the semaphore without a timeout
    async with sem:
        # Once acquired, the AI call itself is bounded by wait_for to prevent hanging
        return await asyncio.wait_for(
            provider.classify_text(text, context=context, lang=lang, chat_settings=settings),
            timeout=5.0
        )"""
text = text.replace(old_func, new_func)

old_img_func = """async def _classify_image_with_semaphore(sem, provider, image, caption, lang, settings):
    async with sem:
        return await provider.classify_image(image, caption=caption, lang=lang, chat_settings=settings)"""

new_img_func = """async def _classify_image_with_semaphore(sem, provider, image, caption, lang, settings):
    async with sem:
        return await asyncio.wait_for(
            provider.classify_image(image, caption=caption, lang=lang, chat_settings=settings),
            timeout=5.0
        )"""
text = text.replace(old_img_func, new_img_func)

# Now we must remove wait_for from the callers!
text = re.sub(
    r'verdict = await asyncio\.wait_for\(\n\s*_classify_with_semaphore\((.*?)\),\n\s*timeout=5\.0\n\s*\)',
    r'verdict = await _classify_with_semaphore(\1)',
    text
)
text = re.sub(
    r'verdict = await asyncio\.wait_for\(\n\s*_classify_image_with_semaphore\((.*?)\),\n\s*timeout=5\.0\n\s*\)',
    r'verdict = await _classify_image_with_semaphore(\1)',
    text
)

with open('src/redqueen/handlers/ai_review.py', 'w') as f:
    f.write(text)

