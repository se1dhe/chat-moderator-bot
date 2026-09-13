with open('src/pages/settings/Modes.tsx', 'r') as f:
    content = f.read()

old_range = """        <Row title={t('modes.nightRange')} value={`${m.night.start}:00 \u2013 ${m.night.end}:00`}>
          <div className="flex gap-2">
            <Stepper value={m.night.start} min={0} max={23} onChange={(v) => s.updateSection('modes', { night: { ...m.night, start: v } })} />
            <Stepper value={m.night.end} min={0} max={23} onChange={(v) => s.updateSection('modes', { night: { ...m.night, end: v } })} />
          </div>
        </Row>"""

if old_range not in content:
    # try with different hyphen
    old_range = """        <Row title={t('modes.nightRange')} value={`${m.night.start}:00 – ${m.night.end}:00`}>
          <div className="flex gap-2">
            <Stepper value={m.night.start} min={0} max={23} onChange={(v) => s.updateSection('modes', { night: { ...m.night, start: v } })} />
            <Stepper value={m.night.end} min={0} max={23} onChange={(v) => s.updateSection('modes', { night: { ...m.night, end: v } })} />
          </div>
        </Row>"""

new_range = """        <div className="flex flex-col gap-3 px-2 py-3 border-t border-neutral-100 dark:border-neutral-800/50 mt-1">
          <div className="flex justify-between items-center w-full">
            <span className="text-sm font-semibold text-neutral-900 dark:text-neutral-50 leading-tight">{t('modes.nightRange')}</span>
            <span className="text-sm font-medium text-neutral-400 shrink-0">{m.night.start}:00 – {m.night.end}:00</span>
          </div>
          <div className="flex gap-2 w-full items-center justify-between">
            <div className="flex-1 flex justify-center"><Stepper value={m.night.start} min={0} max={23} onChange={(v) => s.updateSection('modes', { night: { ...m.night, start: v } })} /></div>
            <span className="text-neutral-400 font-bold">—</span>
            <div className="flex-1 flex justify-center"><Stepper value={m.night.end} min={0} max={23} onChange={(v) => s.updateSection('modes', { night: { ...m.night, end: v } })} /></div>
          </div>
        </div>"""

content = content.replace(old_range, new_range)

with open('src/pages/settings/Modes.tsx', 'w') as f:
    f.write(content)

print("Fixed Modes!")
