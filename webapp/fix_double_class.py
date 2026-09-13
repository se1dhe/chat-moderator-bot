import os
import re

def fix_file(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r') as f:
        content = f.read()

    # Find elements with multiple className="..." props on the same line/element and merge them
    # Because they might be on multiple lines, we can just do a regex replace for `className="A" className="B"` -> `className="A B"`
    
    # Simple regex to catch cases where they are close:
    pattern1 = re.compile(r'className="([^"]+)"\s+className="([^"]+)"')
    while pattern1.search(content):
        content = pattern1.sub(r'className="\1 \2"', content)
        
    with open(filepath, 'w') as f:
        f.write(content)

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.tsx'):
            fix_file(os.path.join(root, file))

print("Fixed double classes!")
