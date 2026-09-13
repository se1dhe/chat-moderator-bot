import re

with open('webapp/src/pages/Dashboard.tsx', 'r') as f:
    text = f.read()

# Add ShieldAlert to imports
text = text.replace("import {\n  ShieldCheck,", "import {\n  ShieldCheck, ShieldAlert,")

# Replace ShieldAlertCheck with ShieldCheck
text = text.replace("ShieldAlertCheck", "ShieldCheck")

with open('webapp/src/pages/Dashboard.tsx', 'w') as f:
    f.write(text)

