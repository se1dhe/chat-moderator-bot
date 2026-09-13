with open('webapp/src/pages/settings/Defcon.tsx', 'r') as f:
    text = f.read()
if 'showAlert' not in text:
    text = text.replace("import { Toggle", "import { showAlert } from '../../lib/telegram'\nimport { Toggle")

text = text.replace("<Row title={t('defcon.threshold')}", "<Row title={t('defcon.threshold')} onInfo={() => showAlert(t('defcon.info.threshold'))}")

with open('webapp/src/pages/settings/Defcon.tsx', 'w') as f:
    f.write(text)

with open('webapp/src/pages/settings/AI.tsx', 'r') as f:
    text = f.read()
if 'showAlert' not in text:
    text = text.replace("import { Toggle", "import { showAlert } from '../../lib/telegram'\nimport { Toggle")

text = text.replace("<Row title={t('ai.log_channel')}", "<Row title={t('ai.log_channel')} onInfo={() => showAlert(t('ai.info.log'))}")
text = text.replace("<div className=\"text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2\">{t('ai.mode')}</div>", "<div className=\"text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2 flex items-center justify-between\">{t('ai.mode')} <button onClick={() => showAlert(t('ai.info.mode'))} className=\"text-neutral-400 hover:text-blue-500 mr-1\"><svg width=\"15\" height=\"15\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" strokeWidth=\"2\" strokeLinecap=\"round\" strokeLinejoin=\"round\"><circle cx=\"12\" cy=\"12\" r=\"10\"/><path d=\"M12 16v-4\"/><path d=\"M12 8h.01\"/></svg></button></div>")

with open('webapp/src/pages/settings/AI.tsx', 'w') as f:
    f.write(text)

