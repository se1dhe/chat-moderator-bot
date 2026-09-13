import re

with open('webapp/src/i18n/translations.ts', 'r') as f:
    text = f.read()

text = text.replace("'sec.raid.desc': 'Lockdown on massive join spikes',", "'sec.defcon.desc': 'Lockdown on massive join spikes',")
text = text.replace("'sec.raid.desc': 'Блокировка при массовых вступлениях',", "'sec.defcon.desc': 'Блокировка при спам-атаках',")
text = text.replace("'sec.raid.desc': 'Блокування при масових вступах',", "'sec.defcon.desc': 'Блокування при спам-атаках',")

text = text.replace("'tips.raid': 'Anti-Raid is off, your group is vulnerable.',", "'tips.defcon': 'Auto-DEFCON is off, your group is vulnerable to spam spikes.',")
text = text.replace("'tips.raid': 'Анти-Рейд выключен, ваша группа уязвима.',", "'tips.defcon': 'Auto-DEFCON выключен, ваша группа уязвима для атак.',")
text = text.replace("'tips.raid': 'Анти-Рейд вимкнений, ваша група вразлива.',", "'tips.defcon': 'Auto-DEFCON вимкнено, ваша група вразлива для атак.',")

with open('webapp/src/i18n/translations.ts', 'w') as f:
    f.write(text)

