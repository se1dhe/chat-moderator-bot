import re
with open('src/redqueen/handlers/__init__.py', 'r') as f:
    text = f.read()

text = text.replace('    raid,\n', '    defcon,\n    summary,\n')
text = text.replace('    dp.include_router(raid.router)\n', '    dp.include_router(defcon.router)\n    dp.include_router(summary.router)\n')

with open('src/redqueen/handlers/__init__.py', 'w') as f:
    f.write(text)
