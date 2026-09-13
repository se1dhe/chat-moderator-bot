with open('webapp/src/pages/settings/AI.tsx', 'r') as f:
    text = f.read()

# Define the block to remove
block_to_remove = """      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('ai.log_channel')}</div>
      <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60 rounded-2xl p-4 mb-4 shadow-sm w-full">
        <div className="text-[13px] font-semibold mb-2">{t('ai.log_channel.desc')}</div>
        <input 
          className="w-full px-4 py-3 bg-neutral-50 dark:bg-black border border-neutral-200 dark:border-neutral-800/60 rounded-xl focus:outline-none focus:border-primary/50 transition-colors font-medium text-[15px]" 
          type="text"
          placeholder="-100..."
          value={s.draft.log_channel_id || ''}
          onChange={(e) => s.setSection('log_channel_id', e.target.value ? Number(e.target.value) : null)}
        />
      </div>"""

if block_to_remove in text:
    text = text.replace(block_to_remove, "")
else:
    print("Block not found exactly as string. Will try regex.")
    import re
    text = re.sub(r'<div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">\{t\(\'ai\.log_channel\'\)\}</div>.*?</div>\s*</div>', '', text, flags=re.DOTALL)

with open('webapp/src/pages/settings/AI.tsx', 'w') as f:
    f.write(text)
