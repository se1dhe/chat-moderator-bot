import re

with open('webapp/src/pages/Dashboard.tsx', 'r') as f:
    text = f.read()

if 'PresetsGallery' not in text:
    text = text.replace("import { AISummary } from '../components/AISummary';", "import { AISummary } from '../components/AISummary';\nimport { PresetsGallery } from '../components/PresetsGallery';")
    
    text = text.replace("<motion.div variants={item}><ProBanner /></motion.div>", "<motion.div variants={item}><ProBanner /></motion.div>\n\n      <motion.div variants={item}><PresetsGallery /></motion.div>")

with open('webapp/src/pages/Dashboard.tsx', 'w') as f:
    f.write(text)
