import re

with open('src/pages/Dashboard.tsx', 'r') as f:
    content = f.read()

# Remove the root tailwind animation
content = content.replace(
    'className="w-full flex flex-col gap-4 animate-in fade-in slide-in-from-bottom-2 duration-300"',
    'className="w-full flex flex-col gap-4"'
)

# Replace the return ( <div with return ( <motion.div variants={container} initial="hidden" animate="show"
content = content.replace(
    'return (\n    <div className="w-full flex flex-col gap-4"',
    'return (\n    <motion.div variants={container} initial="hidden" animate="show" className="w-full flex flex-col gap-4"'
)
# And the closing tag
content = re.sub(r'    </div>\n  \);\n}', '    </motion.div>\n  );\n}', content)

# Inject the variants definition before return (
variants = """
  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.03
      }
    }
  };

  const item = {
    hidden: { opacity: 0, y: 8, scale: 0.97 },
    show: { opacity: 1, y: 0, scale: 1, transition: { type: "spring", stiffness: 500, damping: 30, mass: 0.5 } }
  };

  return (
"""
content = content.replace('  return (\n', variants)

# Add variants={item} to ProBanner, Tips, Lang block, Privacy block
content = content.replace('<ProBanner />', '<motion.div variants={item}><ProBanner /></motion.div>')
content = content.replace('<Tips chatId={cid} />', '<motion.div variants={item}><Tips chatId={cid} /></motion.div>')

# For the Lang block
lang_block = """      <div>
        <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider mb-2 ml-1">{t('dash.chatLang')}</div>
        <Segmented value={draft.lang} onChange={(v: string) => setSection('lang', v)} options={LANGS} />
      </div>"""
new_lang = """      <motion.div variants={item}>
        <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider mb-2 ml-1">{t('dash.chatLang')}</div>
        <Segmented value={draft.lang} onChange={(v: string) => setSection('lang', v)} options={LANGS} />
      </motion.div>"""
content = content.replace(lang_block, new_lang)

# For the Privacy block
priv_block = """      <div>
        <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider mb-2 ml-1">{t('dash.privacy')}</div>
        <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60 rounded-2xl p-4 shadow-sm">
          <Row title={t('dash.privacy')} desc={t('dash.privacy.desc')}>
            <Toggle 
              checked={draft.core.anonymize_events ?? false}
              onChange={(v: boolean) => setSection('core', { ...draft.core, anonymize_events: v })}
            />
          </Row>
        </div>
      </div>"""
new_priv = """      <motion.div variants={item}>
        <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider mb-2 ml-1">{t('dash.privacy')}</div>
        <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60 rounded-2xl p-4 shadow-sm">
          <Row title={t('dash.privacy')} desc={t('dash.privacy.desc')}>
            <Toggle 
              checked={draft.core.anonymize_events ?? false}
              onChange={(v: boolean) => setSection('core', { ...draft.core, anonymize_events: v })}
            />
          </Row>
        </div>
      </motion.div>"""
content = content.replace(priv_block, new_priv)

# For groups, remove variants={container} initial="hidden" animate="show" if it exists (it doesn't, we removed it)
# We just need to change <motion.div key={g.label} className="w-full flex flex-col gap-2"> to use variants={item} for the label?
# No, let's just apply variants={item} to the label, and let the group itself just be a normal div, but wait, staggerChildren works down the tree!
# Actually, if we wrap the group label in variants={item}, and the buttons in variants={item}, it will stagger them ALL perfectly!

# Find the group mapping
content = content.replace(
    '<motion.div key={g.label}  className="w-full flex flex-col gap-2">',
    '<div key={g.label} className="w-full flex flex-col gap-2">'
)
content = content.replace(
    '          <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider mt-2 ml-1">{g.label}</div>',
    '          <motion.div variants={item} className="text-sm font-semibold text-neutral-500 uppercase tracking-wider mt-2 ml-1">{g.label}</motion.div>'
)

# And add variants={item} to the motion.button inside the map
content = content.replace(
    '                <motion.button\n                  whileTap={{ scale: 0.97 }}',
    '                <motion.button\n                  variants={item}\n                  whileTap={{ scale: 0.97 }}'
)

with open('src/pages/Dashboard.tsx', 'w') as f:
    f.write(content)

print("Fixed Dashboard with premium animations!")
