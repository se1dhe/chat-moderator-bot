with open('webapp/src/pages/settings/AI.tsx', 'r') as f:
    text = f.read()

new_log_channel = """
      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('ai.log_channel')}</div>
      <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60 rounded-2xl p-4 mb-4 shadow-sm w-full">
        <div className="text-[13px] font-semibold mb-2">{t('ai.log_channel.desc')}</div>
        <input 
          className="w-full px-4 py-3 bg-neutral-50 dark:bg-black border border-neutral-200 dark:border-neutral-800/60 rounded-xl focus:outline-none focus:border-primary/50 transition-colors font-medium text-[15px]" 
          type="text"
          placeholder="-100..."
          value={s.draft.log_channel_id || ''}
          onChange={(e) => s.updateSection('log_channel_id', e.target.value ? Number(e.target.value) : null)}
        />
      </div>

      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('ai.mode')}</div>"""

text = text.replace("      <div className=\"text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2\">{t('ai.mode')}</div>", new_log_channel)

with open('webapp/src/pages/settings/AI.tsx', 'w') as f:
    f.write(text)
