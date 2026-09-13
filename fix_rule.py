with open('src/redqueen/services/quarantine.py', 'r') as f:
    text = f.read()

old_rule = """    if action == "rule" and verdict.text:
        chat_settings = await repo.get_settings(session, verdict.chat_telegram_id)
        words = get_config(chat_settings)["filters"]["banned_words"]
        snippet = verdict.text.strip().lower()[:60]
        if snippet and snippet not in words:
            words.append(snippet)
            save_section(chat_settings, "filters", {"banned_words": words})"""

# Take up to 200 chars, but don't cut words in half if possible.
# Actually, just taking up to 200 characters is extremely specific and won't cause false positives.
new_rule = """    if action == "rule" and verdict.text:
        chat_settings = await repo.get_settings(session, verdict.chat_telegram_id)
        words = get_config(chat_settings)["filters"]["banned_words"]
        # Take up to 200 chars to ensure high specificity and avoid banning generic prefixes like "Hello"
        snippet = verdict.text.strip().lower()[:200].strip()
        if snippet and snippet not in words:
            words.append(snippet)
            save_section(chat_settings, "filters", {"banned_words": words})"""

text = text.replace(old_rule, new_rule)

with open('src/redqueen/services/quarantine.py', 'w') as f:
    f.write(text)

