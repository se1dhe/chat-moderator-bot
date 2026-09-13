with open('webapp/src/pages/SettingsSection.tsx', 'r') as f:
    text = f.read()

text = text.replace("import Raid from './settings/Raid'", "import Defcon from './settings/Defcon'")
text = text.replace("case 'raid': return <Raid s={s} t={t} />", "case 'defcon': return <Defcon s={s} t={t} />")

with open('webapp/src/pages/SettingsSection.tsx', 'w') as f:
    f.write(text)
