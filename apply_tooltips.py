import re

def insert_alert_import(file_path):
    with open(file_path, 'r') as f:
        text = f.read()
    if 'showAlert' not in text:
        text = text.replace("import { Toggle", "import { showAlert } from '../../lib/telegram'\nimport { Toggle")
    with open(file_path, 'w') as f:
        f.write(text)

def replace_in_file(file_path, replacements):
    with open(file_path, 'r') as f:
        text = f.read()
    for old, new in replacements.items():
        text = text.replace(old, new)
    with open(file_path, 'w') as f:
        f.write(text)


insert_alert_import('webapp/src/pages/settings/Captcha.tsx')
replace_in_file('webapp/src/pages/settings/Captcha.tsx', {
    "<Row title={t('captcha.timeout')}": "<Row title={t('captcha.timeout')} onInfo={() => showAlert(t('captcha.info.timeout'))}"
})


insert_alert_import('webapp/src/pages/settings/Antiflood.tsx')
replace_in_file('webapp/src/pages/settings/Antiflood.tsx', {
    "<Row title={t('cat.flood')}": "<Row title={t('cat.flood')} onInfo={() => showAlert(t('antiflood.info.messages'))}",
    "<Row title={t('antiflood.window')}": "<Row title={t('antiflood.window')} onInfo={() => showAlert(t('antiflood.info.window'))}"
})


insert_alert_import('webapp/src/pages/settings/Filters.tsx')
replace_in_file('webapp/src/pages/settings/Filters.tsx', {
    "<Row title={t('filters.links')}": "<Row title={t('filters.links')} onInfo={() => showAlert(t('filters.info.links'))}",
    "<Row title={t('filters.forwards')}": "<Row title={t('filters.forwards')} onInfo={() => showAlert(t('filters.info.forwards'))}",
    "<Row title={t('filters.badwords')}": "<Row title={t('filters.badwords')} onInfo={() => showAlert(t('filters.info.badwords'))}",
})


insert_alert_import('webapp/src/pages/settings/Modes.tsx')
replace_in_file('webapp/src/pages/settings/Modes.tsx', {
    "<Row title={t('modes.readonly')}": "<Row title={t('modes.readonly')} onInfo={() => showAlert(t('modes.info.readonly'))}",
    "<Row title={t('modes.slowmode')}": "<Row title={t('modes.slowmode')} onInfo={() => showAlert(t('modes.info.slowmode'))}",
})

