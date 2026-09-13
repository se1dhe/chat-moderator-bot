with open('webapp/src/pages/SettingsSection.tsx', 'r') as f:
    text = f.read()

text = text.replace("raid: <Raid s={s} t={t} />", "defcon: <Defcon s={s} t={t} />")

with open('webapp/src/pages/SettingsSection.tsx', 'w') as f:
    f.write(text)
