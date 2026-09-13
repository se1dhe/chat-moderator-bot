import { useState, useEffect, useRef } from 'react'
import { Plus, Lock } from 'lucide-react'
import { Toggle, Row, Segmented, Stepper, Slider, Chips, Spinner } from '../../components/ui'
import { haptic, showAlert } from '../../lib/telegram'
import { api } from '../../lib/api'

export default function Modes({ s, t }) {
  const m = s.draft.modes
  return (
    <>
      <div className="section-label">{t('modes.night')}</div>
      <div className="card">
        <Row title={t('modes.night')}>
          <Toggle checked={m.night.enabled} onChange={(v) => s.updateSection('modes', { night: { ...m.night, enabled: v } })} />
        </Row>
        <Row title={t('modes.nightRange')} value={`${m.night.start}:00 – ${m.night.end}:00`}>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <Stepper value={m.night.start} min={0} max={23} onChange={(v) => s.updateSection('modes', { night: { ...m.night, start: v } })} />
            <Stepper value={m.night.end} min={0} max={23} onChange={(v) => s.updateSection('modes', { night: { ...m.night, end: v } })} />
          </div>
        </Row>
      </div>
      <div className="card">
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
