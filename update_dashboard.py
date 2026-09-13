with open('webapp/src/pages/Dashboard.tsx', 'r') as f:
    text = f.read()

text = text.replace("import Raid from './settings/Raid'", "import Defcon from './settings/Defcon'")
text = text.replace("<Raid s={s} t={t} />", "<Defcon s={s} t={t} />")
text = text.replace("id: 'raid'", "id: 'defcon'")
text = text.replace("icon: Shield", "icon: ShieldAlert")
text = text.replace("label: t('sec.raid')", "label: t('sec.defcon')")
text = text.replace("import { Settings2,", "import { Settings2, ShieldAlert,")

with open('webapp/src/pages/Dashboard.tsx', 'w') as f:
    f.write(text)
