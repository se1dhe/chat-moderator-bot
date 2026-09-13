with open('webapp/src/pages/Dashboard.tsx', 'r') as f:
    text = f.read()
text = text.replace("key: 'raid'", "key: 'defcon'")
text = text.replace("t('sec.raid')", "t('sec.defcon')")
text = text.replace("t('sec.raid.desc')", "t('sec.defcon.desc')")
text = text.replace("draft.raid.enabled", "draft.defcon?.enabled")
with open('webapp/src/pages/Dashboard.tsx', 'w') as f:
    f.write(text)

with open('webapp/src/components/Tips.tsx', 'r') as f:
    text = f.read()
text = text.replace("d.raid.enabled", "d.defcon?.enabled")
text = text.replace("'tips.raid'", "'tips.defcon'")
with open('webapp/src/components/Tips.tsx', 'w') as f:
    f.write(text)

