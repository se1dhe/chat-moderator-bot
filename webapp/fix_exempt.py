with open('src/pages/settings/Exempt.tsx', 'r') as f:
    content = f.read()

content = content.replace('<div className="chip-input">', '<div className="flex flex-col gap-3 mt-3">')

with open('src/pages/settings/Exempt.tsx', 'w') as f:
    f.write(content)

print("Fixed Exempt!")
