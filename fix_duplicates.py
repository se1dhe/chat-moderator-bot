import re

with open('webapp/src/i18n/translations.ts', 'r') as f:
    text = f.read()

# For each section (en, ru, uk), remove duplicate rbac keys
def dedupe(block):
    lines = block.split('\n')
    seen = set()
    out = []
    for line in lines:
        m = re.search(r"'([^']+)':", line)
        if m:
            k = m.group(1)
            if k in seen:
                continue
            seen.add(k)
        out.append(line)
    return '\n'.join(out)

new_text = dedupe(text)

with open('webapp/src/i18n/translations.ts', 'w') as f:
    f.write(new_text)
