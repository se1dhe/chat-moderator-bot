import re

with open('webapp/src/pages/Dashboard.tsx', 'r') as f:
    text = f.read()

text = text.replace("import { Tips } from '../components/Tips';", "import { Tips } from '../components/Tips';\nimport { AISummary } from '../components/AISummary';")

old_overview = """      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('sec.overview')}</div>
      <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60 rounded-2xl p-2 mb-4 shadow-sm w-full">"""

new_overview = """      <AISummary t={t} />
      
      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('sec.overview')}</div>
      <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60 rounded-2xl p-2 mb-4 shadow-sm w-full">"""

text = text.replace(old_overview, new_overview)

with open('webapp/src/pages/Dashboard.tsx', 'w') as f:
    f.write(text)
