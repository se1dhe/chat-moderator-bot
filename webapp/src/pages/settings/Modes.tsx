import { useState, useEffect, useRef } from 'react'
import { Plus, Lock } from 'lucide-react'
import { Toggle, Row, Segmented, Stepper, Slider, Chips, Spinner } from '../../components/ui'
import { haptic, showAlert } from '../../lib/telegram'
import { api } from '../../lib/api'

export default function Modes({ s, t }) {
  const m = s.draft.modes
  return (
    <>
      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('modes.night')}</div>
      <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60 rounded-2xl p-2 mb-4 shadow-sm w-full">
        <Row title={t('modes.night')}>
          <Toggle checked={m.night.enabled} onChange={(v) => s.updateSection('modes', { night: { ...m.night, enabled: v } })} />
        </Row>
        <div className="flex flex-col gap-3 px-2 py-3 border-t border-neutral-100 dark:border-neutral-800/50 mt-1">
          <div className="flex justify-between items-center w-full">
            <span className="text-sm font-semibold text-neutral-900 dark:text-neutral-50 leading-tight">{t('modes.nightRange')}</span>
            <span className="text-sm font-medium text-neutral-400 shrink-0">{m.night.start}:00 – {m.night.end}:00</span>
          </div>
          <div className="flex gap-2 w-full items-center justify-between">
            <div className="flex-1 flex justify-center"><Stepper value={m.night.start} min={0} max={23} onChange={(v) => s.updateSection('modes', { night: { ...m.night, start: v } })} /></div>
            <span className="text-neutral-400 font-bold">—</span>
            <div className="flex-1 flex justify-center"><Stepper value={m.night.end} min={0} max={23} onChange={(v) => s.updateSection('modes', { night: { ...m.night, end: v } })} /></div>
          </div>
        </div>
      </div>
      <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60 rounded-2xl p-2 mb-4 shadow-sm w-full">
        <Row title={t('settings.crossChatTitle')} desc={t('settings.crossChatDesc')}>
          <Toggle checked={m.use_global_bans || false} onChange={(v) => s.updateSection('modes', { use_global_bans: v })} />
        </Row>

        <Row title={t('modes.silent')} desc={t('modes.silentDesc')}>
          <Toggle checked={m.silent} onChange={(v) => s.updateSection('modes', { silent: v })} />
        </Row>
        <Row title={t('modes.slow')} desc={t('modes.slowDesc')} value={`${m.slow_seconds} ${t('common.seconds')}`}>
          <Stepper value={m.slow_seconds} min={0} max={3600} step={5} onChange={(v) => s.updateSection('modes', { slow_seconds: v })} />
        </Row>
      </div>
    </>
  )
}
