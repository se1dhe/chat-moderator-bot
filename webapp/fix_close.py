with open('src/pages/Dashboard.tsx', 'r') as f:
    lines = f.readlines()

lines[197] = '        </div>\n'

with open('src/pages/Dashboard.tsx', 'w') as f:
    f.writelines(lines)
