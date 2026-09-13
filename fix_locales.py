import os

for lang, val in [("ru", "'{name}' забанен Глобальной Сетью Доверия (заблокирован {count} админами)."), 
                  ("en", "'{name}' was banned by the Global Network of Trust (blocked by {count} admins)."), 
                  ("uk", "'{name}' забанений Глобальною Мережею Довіри (заблокований {count} адмінами).")]:
    with open(f'src/redqueen/locales/{lang}.py', 'r') as f:
        text = f.read()
    
    text = text.replace('"GLOBAL_BANNED":', f'"NOT_BANNED": "{val}",\n    "GLOBAL_BANNED":')
    with open(f'src/redqueen/locales/{lang}.py', 'w') as f:
        f.write(text)

