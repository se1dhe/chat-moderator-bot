import re

with open("src/pages/SettingsSection.jsx", "r") as f:
    content = f.read()

content = content.replace("import { haptic } from '../lib/telegram'", "import { haptic } from '../lib/telegram'\nimport { api } from '../lib/api'")
content = content.replace("{c.media_url ? 'Media attached' : 'No media'}", "{c.media_url ? t('common.mediaAttached') : t('common.noMedia')}")
content = content.replace('<button className="text-[13px] text-red-500" onClick={() => s.updateSection(\'auto_comment\', { media_url: \'\' })}>Remove media</button>', '<button className="text-[13px] text-red-500" onClick={() => s.updateSection(\'auto_comment\', { media_url: \'\' })}>{t("common.removeMedia")}</button>')
content = content.replace('<button className="text-[13px] text-red-500" onClick={() => s.updateSection(\'auto_comment\', { media_url: \'\' })}>\n                Remove media\n              </button>', '<button className="text-[13px] text-red-500" onClick={() => s.updateSection(\'auto_comment\', { media_url: \'\' })}>{t("common.removeMedia")}</button>')

with open("src/pages/SettingsSection.jsx", "w") as f:
    f.write(content)

tips = {
    'common.noMedia': ['No media', 'Нет медиа', 'Немає медіа'],
    'common.mediaAttached': ['Media attached', 'Медиа прикреплено', 'Медіа прикріплено'],
    'common.removeMedia': ['Remove media', 'Удалить медиа', 'Видалити медіа']
}

with open("src/i18n/translations.js", "r") as f:
    t_content = f.read()

def insert_keys(lang_content, lang_idx):
    lines = []
    for k, v in tips.items():
        val = v[lang_idx].replace("'", "\\'")
        lines.append(f"    '{k}': '{val}',")
    return "\n".join(lines) + "\n"

en_part = re.search(r'(en: \{)(.*?)(  \},)', t_content, re.DOTALL)
ru_part = re.search(r'(ru: \{)(.*?)(  \},)', t_content, re.DOTALL)
uk_part = re.search(r'(uk: \{)(.*?)(  \})', t_content, re.DOTALL)

t_content = t_content.replace(en_part.group(1) + en_part.group(2), en_part.group(1) + "\n" + insert_keys(en_part.group(2), 0) + en_part.group(2))
t_content = t_content.replace(ru_part.group(1) + ru_part.group(2), ru_part.group(1) + "\n" + insert_keys(ru_part.group(2), 1) + ru_part.group(2))
t_content = t_content.replace(uk_part.group(1) + uk_part.group(2), uk_part.group(1) + "\n" + insert_keys(uk_part.group(2), 2) + uk_part.group(2))

with open("src/i18n/translations.js", "w") as f:
    f.write(t_content)
