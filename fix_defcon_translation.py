with open('webapp/src/i18n/translations.ts', 'r') as f:
    text = f.read()

# I will just use regex to replace the 2nd and 3rd occurrences of 'sec.defcon': 'Auto-DEFCON'
# English is first (lines 1-300), RU is second (300-600), UK is third (600-900).

parts = text.split("'sec.defcon': 'Auto-DEFCON',")

if len(parts) == 4:
    text = parts[0] + "'sec.defcon': 'Auto-DEFCON'," + parts[1] + "'sec.defcon': 'Авто-Защита'," + parts[2] + "'sec.defcon': 'Авто-Захист'," + parts[3]

with open('webapp/src/i18n/translations.ts', 'w') as f:
    f.write(text)

