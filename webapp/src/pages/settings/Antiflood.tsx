import { useState, useEffect, useRef } from 'react'
import { Plus, Lock } from 'lucide-react'
import { Toggle, Row, Segmented, Stepper, Slider, Chips, Spinner } from '../../components/ui'
import { haptic, showAlert } from '../../lib/telegram'
import { api } from '../../lib/api'

const mins = (sec) => Math.round(sec / 60)

export default function Antiflood({ s, t }) {
  const a = s.draft.antiflood
  return (
    <>
      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('sec.antiflood')}</div>
      <div className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-2xl p-2 mb-4 shadow-sm w-full">
        <Row title={t('antiflood.enabled')}>
          <Toggle checked={a.enabled} onChange={(v) => s.updateSection('antiflood', { enabled: v })} />
        </Row>
        <Row title={t('antiflood.limit')} value={a.limit}>
          <Stepper value={a.limit} min={2} max={50} onChange={(v) => s.updateSection('antiflood', { limit: v })} />
        </Row>
        <Row title={t('antiflood.window')} value={`${a.window} ${t('common.seconds')}`}>
          <Stepper value={a.window} min={2} max={300} step={1} onChange={(v) => s.updateSection('antiflood', { window: v })} />
        </Row>
        <Row title={t('antiflood.muteSeconds')} value={`${mins(a.mute_seconds)} ${t('common.minutes')}`}>
          <Stepper value={mins(a.mute_seconds)} min={1} max={1440} onChange={(v) => s.updateSection('antiflood', { mute_seconds: v * 60 })} />
        </Row>
      </div>
      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('antiflood.action')}</div>
      <Segmented value={a.action} onChange={(v) => s.updateSection('antiflood', { action: v })}
        options={[
          { value: 'mute', label: t('action.mute') },
          { value: 'kick', label: t('action.kick') },
          { value: 'ban', label: t('action.ban') },
        ]} />
      {a.action === 'ban' && (
        <div className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-2xl p-2 mb-4 shadow-sm w-full" style={{ marginTop: '0.75rem' }}>
          <Row title={t('antiflood.banSeconds')}
            value={mins(a.ban_seconds) <= 0 ? t('dur.perm') : `${mins(a.ban_seconds)} ${t('common.minutes')}`}>
            <Stepper value={mins(a.ban_seconds)} min={0} max={7 * 1440} step={60}
              onChange={(v) => s.updateSection('antiflood', { ban_seconds: v * 60 })} />
          </Row>
        </div>
      )}
    </>
  )
}
