import os

def replace_in_file(filepath, replacements):
    if not os.path.exists(filepath): return
    with open(filepath, 'r') as f:
        content = f.read()
    
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    with open(filepath, 'w') as f:
        f.write(content)

replacements = {
    'className="row-desc"': 'className="text-[13px] text-neutral-500 leading-snug"',
    'className="badge badge-gold"': 'className="px-2 py-0.5 bg-amber-100 text-amber-700 dark:bg-amber-500/20 dark:text-amber-400 rounded-md text-[11px] font-bold uppercase tracking-wider"',
    'className="badge badge-danger"': 'className="px-2 py-0.5 bg-red-100 text-red-700 dark:bg-red-500/20 dark:text-red-400 rounded-md text-[11px] font-bold uppercase tracking-wider inline-flex items-center gap-1"',
    'className="card-pad"': 'className="p-4"',
    '''style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}''': 'className="flex flex-col gap-3"',
    '''style={{ display: 'flex', flexDirection: 'column', gap: '0.9rem' }}''': 'className="flex flex-col gap-3"',
    '''style={{ marginTop: '0.5rem', fontWeight: 600, fontSize: '15px' }}''': 'className="mt-2 font-semibold text-[15px]"',
    '''style={{ fontWeight: 600, fontSize: '15px', marginTop: '0.5rem' }}''': 'className="mt-2 font-semibold text-[15px]"',
    '''style={{ minHeight: '80px', resize: 'vertical' }}''': 'className="min-h-[80px] resize-y"',
    '''style={{ minHeight: '120px', resize: 'vertical' }}''': 'className="min-h-[120px] resize-y"',
    '''style={{ marginTop: '1.5rem' }}''': 'className="mt-6"',
    '''style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}''': 'className="flex justify-between items-center"',
    '''style={{ fontFamily: 'monospace', color: 'var(--tg-theme-accent-color)', fontWeight: 600 }}''': 'className="font-mono text-primary font-semibold"',
    '''style={{ padding: '4px 10px', fontSize: '13px' }}''': 'className="px-3 py-1 text-[13px]"',
    '''style={{ padding: '0.3rem 0.6rem', fontSize: '12px' }}''': 'className="px-2.5 py-1 text-xs"',
    '''style={{ fontSize: '14px', color: 'var(--tg-theme-text-color)' }}''': 'className="text-sm text-neutral-700 dark:text-neutral-300"',
    '''style={{ marginLeft: '6px' }}''': 'className="ml-1.5"',
    '''style={{ display: 'flex', alignItems: 'center', gap: '0.7rem' }}''': 'className="flex items-center gap-3"',
    '''style={{ marginTop: '0.75rem' }}''': 'className="mt-3"',
    '''style={{ display: 'flex', gap: '0.5rem' }}''': 'className="flex gap-2"',
    '''style={{ margin: '0.5rem 0.2rem 0' }}''': 'className="mt-2 mx-1"',
    '''style={{ marginTop: '0.75rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}''': 'className="mt-3 flex flex-col gap-2"',
    '''style={{ padding: '0.75rem 1rem' }}''': 'className="px-4 py-3"',
    '''style={{ padding: '0 1rem 0.75rem' }}''': 'className="px-4 pb-3"',
    '''style={{ fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.25rem' }}''': 'className="text-[13px] font-semibold mb-1"',
    '''style={{ width: '100%' }}''': 'className="w-full"',
    '''style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.35rem' }}''': 'className="flex justify-between mb-1.5"',
    '''style={{ fontWeight: 600, fontSize: '0.85rem' }}''': 'className="font-semibold text-[13px]"',
    '''style={{ color: overridden ? 'var(--primary-light)' : 'var(--text-muted)' }}''': '',
    '''style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}''': 'className="flex items-center gap-2"',
    '''style={{ color: 'var(--tg-theme-success-color)' }}''': 'className="text-emerald-500"',
    '''className="row-value "''': 'className="text-neutral-500 text-[13px]"',
    '''className={`row-value ${overridden ? '' : ''}`}''': 'className={`text-[13px] ${overridden ? "text-primary" : "text-neutral-500"}`}',
    '''<div className="card-pad" style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>''': '<div className="p-4 flex flex-col gap-2 border-b border-neutral-200 dark:border-neutral-800/50 last:border-0">'
}

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.tsx'):
            replace_in_file(os.path.join(root, file), replacements)

print("Polished styles!")
