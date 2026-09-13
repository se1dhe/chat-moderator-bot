with open('src/pages/settings/Filters.tsx', 'r') as f:
    content = f.read()

content = content.replace('<div className="chip-input">', '<div className="flex flex-col gap-3 mt-3">')

with open('src/pages/settings/Filters.tsx', 'w') as f:
    f.write(content)

print("Fixed Filters!")
