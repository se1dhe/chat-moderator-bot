import re

with open('src/pages/settings/RBAC.tsx', 'r') as f:
    text = f.read()

# Replace <p>Модераторы могут... with <p className="...">...</p> no, just replace the exact string
old_p = "<p>Модераторы могут изменять настройки бота для этой группы.</p>"
new_p = "<p>{t('sec.rbac.desc')}</p>"
text = text.replace(old_p, new_p)

# Replace alert/confirm
text = text.replace("import { useState, useEffect } from 'react';", "import { useState, useEffect } from 'react';\nimport { showAlert, showConfirm } from '../../lib/telegram';")

text = text.replace(
    "if (!confirm(t('rbac_remove_confirm') || 'Are you sure?')) return;",
    "const confirmed = await new Promise(resolve => showConfirm(t('rbac_remove_confirm') || 'Are you sure?', resolve));\n    if (!confirmed) return;"
)

with open('src/pages/settings/RBAC.tsx', 'w') as f:
    f.write(text)
