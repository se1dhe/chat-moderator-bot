import re

with open('src/i18n/translations.ts', 'r') as f:
    text = f.read()

en_block = re.search(r'en: \{(.*?)\},?\n\s*ru: \{', text, re.DOTALL).group(1)
ru_block = re.search(r'ru: \{(.*?)\},?\n\s*uk: \{', text, re.DOTALL).group(1)

en_keys = set(re.findall(r"'([^']+)':", en_block))
ru_keys = set(re.findall(r"'([^']+)':", ru_block))

missing_in_en = ru_keys - en_keys
print("Missing in EN:")
for k in missing_in_en:
    print(k)

