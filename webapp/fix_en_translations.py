with open('src/i18n/translations.ts', 'r') as f:
    content = f.read()

en_add = """    'sec.rbac': 'Roles & Access',
    'sec.rbac.desc': 'Panel access management',
"""

content = content.replace("en: {", "en: {\n" + en_add)

with open('src/i18n/translations.ts', 'w') as f:
    f.write(content)

print("Fixed English translations!")
