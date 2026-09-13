import re

with open('webapp/src/components/PresetsGallery.tsx', 'r') as f:
    text = f.read()

text = text.replace('const { draft, setSection, pro, openUpgrade } = useChatSettings();', 'const { draft, setSection, billing, openPresetPayment } = useChatSettings();')

text = text.replace('const locked = p.pro && !pro;', 'const locked = p.pro && !(billing?.purchased_presets || []).includes(p.id);')

text = text.replace('openUpgrade();', 'openPresetPayment(p.id);')

text = text.replace('<Lock size={14} /> PRO', '<Lock size={14} /> 150 ⭐️')

with open('webapp/src/components/PresetsGallery.tsx', 'w') as f:
    f.write(text)
