import { useState, useEffect, useRef } from 'react'
import { Plus, Lock } from 'lucide-react'
import { Toggle, Row, Segmented, Stepper, Slider, Chips, Spinner } from '../../components/ui'
import { haptic, showAlert } from '../../lib/telegram'
import { api } from '../../lib/api'

const mins = (sec) => Math.round(sec / 60)

const DAY_MIN = 1440

export default function Warns({ s, t }) {
  const core = s.draft.core
  const w = s.draft.warns
  const muteMin = mins(w.mute_seconds)
  const banMin = mins(w.ban_seconds)
  return (
    <>
      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('sec.warns')}</div>
      <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60 rounded-2xl p-2 mb-4 shadow-sm w-full">
        <Row title={t('warns.limit')} value={core.warn_limit}>
          <Stepper value={core.warn_limit} min={1} max={20} onChange={(v) => s.updateSection('core', { warn_limit: v })} />
        </Row>
      </div>
      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('warns.action')}</div>
      <Segmented value={core.warn_action} onChange={(v) => s.updateSection('core', { warn_action: v })}
        options={[
          { value: 'mute', label: t('action.mute') },
          { value: 'kick', label: t('action.kick') },
          { value: 'ban', label: t('action.ban') },
        ]} />

      {core.warn_action === 'mute' && (
        <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60 rounded-2xl p-2 mb-4 shadow-sm w-full mt-3">
          <Row title={t('warns.muteDuration')} value={muteMin <= 0 ? t('dur.perm') : `${muteMin} ${t('common.minutes')}`}>
            <Stepper value={muteMin} min={0} max={7 * DAY_MIN} step={30}
              onChange={(v) => s.updateSection('warns', { mute_seconds: v * 60 })} />
          </Row>
        </div>
      )}
      {core.warn_action === 'ban' && (
        <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60 rounded-2xl p-2 mb-4 shadow-sm w-full mt-3">
          <Row title={t('warns.banDuration')} value={banMin <= 0 ? t('dur.perm') : `${banMin} ${t('common.minutes')}`}>
            <Stepper value={banMin} min={0} max={7 * DAY_MIN} step={60}
              onChange={(v) => s.updateSection('warns', { ban_seconds: v * 60 })} />
          </Row>
        </div>
      )}
    </>
  )
}
