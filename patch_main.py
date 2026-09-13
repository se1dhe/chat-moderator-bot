import sys
c = open('src/redqueen/__main__.py').read()
if "await create_all()" not in c:
    c = c.replace('init_engine(settings.sqlalchemy_dsn)', 'init_engine(settings.sqlalchemy_dsn)\n    from .db.base import create_all\n    await create_all()')
open('src/redqueen/__main__.py', 'w').write(c)
