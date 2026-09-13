import re

css_path = 'webapp/src/styles/index.css'
with open(css_path, 'r') as f:
    css = f.read()

# Add backdrop-filter to card and tile
css = re.sub(r'\.card \{([^}]+)\}', r'.card {\1  backdrop-filter: blur(12px);\n}', css)
css = re.sub(r'\.tile \{([^}]+)\}', r'.tile {\1  backdrop-filter: blur(12px);\n}', css)

# Make sure they use glass-border if they used --border
css = css.replace('border: 1px solid var(--border);', 'border: 1px solid var(--glass-border);')

with open(css_path, 'w') as f:
    f.write(css)

print("Glassmorphism applied")
