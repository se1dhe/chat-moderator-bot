import re

with open('src/pages/settings/Antiflood.tsx', 'r') as f:
    text = f.read()

old_mins = "const mins = (sec) => Math.round(sec / 60)"
new_mins = "const mins = (sec: number | null | undefined) => Math.round((sec || 0) / 60)"

text = text.replace(old_mins, new_mins)

old_def = "export default function Antiflood({ s, t }) {"
new_def = "export default function Antiflood({ s, t }: { s: any, t: any }) {"
text = text.replace(old_def, new_def)

with open('src/pages/settings/Antiflood.tsx', 'w') as f:
    f.write(text)

