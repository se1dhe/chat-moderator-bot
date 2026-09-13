filename = "webapp/src/pages/SettingsSection.jsx"
with open(filename, "r") as f:
    text = f.read()

if "import Triggers from './Triggers'" not in text:
    text = text.replace("import { api } from '../lib/api'", "import { api } from '../lib/api'\nimport Triggers from './Triggers'")
    
with open(filename, "w") as f:
    f.write(text)
