import sys

# Fix KeyError in routes_rbac.py
c = open('src/redqueen/api/routes_rbac.py').read()
c = c.replace('request.app["db_session_maker"]', 'request.app["sessionmaker"]')
open('src/redqueen/api/routes_rbac.py', 'w').write(c)

# We should also ensure the table is created
# Since we don't have alembic, we can just run create_all directly from a script

print("routes_rbac.py fixed")
