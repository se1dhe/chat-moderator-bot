import os
import re

def check_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Find all JSX tags that start with a capital letter (likely icons)
    # and have a className prop that is not a string literal
    pattern = re.compile(r'<([A-Z][a-zA-Z0-9_]*)[^>]*className=\{([^}]*)\}[^>]*>')
    
    for match in pattern.finditer(content):
        tag = match.group(1)
        classname_expr = match.group(2)
        print(f"{filepath}: <{tag} className={{{classname_expr}}}>")

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.tsx') or file.endswith('.jsx'):
            check_file(os.path.join(root, file))

