with open('webapp/src/pages/settings/Defcon.tsx', 'r') as f:
    text = f.read()

old = "<div className=\"text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2\">{t('defcon.action')}</div>"
new = "<div className=\"text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2 flex items-center justify-between\">{t('defcon.action')} <button onClick={() => showAlert(t('defcon.info.action'))} className=\"text-neutral-400 hover:text-blue-500 mr-1\"><svg width=\"15\" height=\"15\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" strokeWidth=\"2\" strokeLinecap=\"round\" strokeLinejoin=\"round\"><circle cx=\"12\" cy=\"12\" r=\"10\"/><path d=\"M12 16v-4\"/><path d=\"M12 8h.01\"/></svg></button></div>"
text = text.replace(old, new)

with open('webapp/src/pages/settings/Defcon.tsx', 'w') as f:
    f.write(text)
