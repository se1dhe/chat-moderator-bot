import re

with open('src/i18n/translations.ts', 'r') as f:
    content = f.read()

ru_add = """    'rbac.title': 'Роли и Доступы',
    'rbac_fetch_error': 'Ошибка загрузки модераторов',
    'rbac_add_error': 'Ошибка добавления модератора',
    'rbac_remove_error': 'Ошибка удаления модератора',
    'rbac_remove_confirm': 'Удалить модератора?',
    'rbac_username_placeholder': 'username или ID',
    'rbac_moderators_list': 'МОДЕРАТОРЫ',
    'rbac_no_moderators': 'Модераторы не добавлены.',
"""

en_add = """    'rbac.title': 'Roles & Access',
    'rbac_fetch_error': 'Error loading moderators',
    'rbac_add_error': 'Error adding moderator',
    'rbac_remove_error': 'Error removing moderator',
    'rbac_remove_confirm': 'Remove moderator?',
    'rbac_username_placeholder': 'username or ID',
    'rbac_moderators_list': 'MODERATORS',
    'rbac_no_moderators': 'No moderators found.',
"""

# Find ru: { and inject
content = content.replace("ru: {", "ru: {\n" + ru_add)
content = content.replace("en: {", "en: {\n" + en_add)

with open('src/i18n/translations.ts', 'w') as f:
    f.write(content)

print("Fixed translations!")
