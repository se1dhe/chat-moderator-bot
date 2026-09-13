import { useState, useEffect, useRef } from 'react'
import { Plus, Lock } from 'lucide-react'
import { Toggle, Row, Segmented, Stepper, Slider, Chips, Spinner } from '../../components/ui'
import { haptic, showAlert } from '../../lib/telegram'
import { api } from '../../lib/api'

const mins = (sec) => Math.round(sec / 60)

export default function Raid({ s, t }) {
  const r = s.draft.raid
  const locked = !s.pro
  return (
    <>
      {locked && (
        <button className="pro-note" onClick={() => s.openUpgrade()}>
          <Lock size={14} />
          <span>{t('pro.raidNote')}</span>
          <span className="px-2 py-0.5 bg-amber-100 text-amber-700 dark:bg-amber-500/20 dark:text-amber-400 rounded-md text-[11px] font-bold uppercase tracking-wider">PRO</span>
        </button>
      )}
      {r.locked && (
        <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60/60/60/60 rounded-2xl p-4 mb-4 shadow-sm w-full flex items-center gap-3">
          <span className="px-2 py-0.5 bg-red-100 text-red-700 dark:bg-red-500/20 dark:text-red-400 rounded-md text-[11px] font-bold uppercase tracking-wider inline-flex items-center gap-1"><Lock size={12} /> {t('raid.locked')}</span>
          <div className="header-spacer" />
          <button className="w-full flex items-center justify-center gap-2 py-3 bg-red-500 hover:bg-red-600 text-white rounded-xl font-bold transition-all active:scale-95 shadow-md shadow-red-500/20 text-[15px]" onClick={() => { haptic('warning'); s.updateSection('raid', { locked: false }) }}>
            {t('raid.unlock')}
          </button>
        </div>
      )}
      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('sec.raid')}</div>
      <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60/60/60/60 rounded-2xl p-2 mb-4 shadow-sm w-full">
        <Row title={t('raid.enabled')}>
          <Toggle checked={r.enabled && !locked} disabled={locked} onDisabledClick={() => s.openUpgrade()}
            onChange={(v) => s.updateSection('raid', { enabled: v })} />
        </Row>
        <Row title={t('raid.threshold')} value={r.join_threshold}>
          <Stepper value={r.join_threshold} min={2} max={100} onChange={(v) => s.updateSection('raid', { join_threshold: v })} />
        </Row>
        <Row title={t('raid.window')} value={`${r.window_seconds} ${t('common.seconds')}`}>
          <Stepper value={r.window_seconds} min={5} max={600} step={5} onChange={(v) => s.updateSection('raid', { window_seconds: v })} />
        </Row>
        <Row title={t('raid.lock')} value={`${mins(r.lock_seconds)} ${t('common.minutes')}`}>
          <Stepper value={mins(r.lock_seconds)} min={1} max={1440} onChange={(v) => s.updateSection('raid', { lock_seconds: v * 60 })} />
        </Row>
      </div>
    </>
  )
}
