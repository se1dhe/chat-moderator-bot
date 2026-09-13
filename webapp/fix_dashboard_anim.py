import re

with open('src/pages/Dashboard.tsx', 'r') as f:
    content = f.read()

# Remove the container and item definitions completely
content = re.sub(r'  const container = \{[\s\S]*?  const item = \{[\s\S]*?  \};\n', '', content)

# Remove variants and initial/animate from motion.div
content = content.replace('variants={container} initial="hidden" animate="show"', '')

# Remove variants from motion.button
content = content.replace('variants={item}\n                  whileTap', 'whileTap')
content = content.replace('variants={item} whileTap', 'whileTap')

# Sometimes formatting might be on one line, so let's use regex for the button too
content = re.sub(r'\s*variants=\{item\}\s*', ' ', content)

with open('src/pages/Dashboard.tsx', 'w') as f:
    f.write(content)

print("Fixed Dashboard animations!")
