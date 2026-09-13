import os
import re

def fix_file(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r') as f:
        content = f.read()

    # fix /60/60/60...
    content = re.sub(r'border-neutral-800(/60)+', 'border-neutral-800/60', content)
    content = re.sub(r'bg-black(/70)+', 'bg-black/70', content)
    content = re.sub(r'bg-black(/80)+', 'bg-black/80', content)
    
    with open(filepath, 'w') as f:
        f.write(content)

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.tsx') or file.endswith('.ts'):
            fix_file(os.path.join(root, file))

print("Fixed classes!")
