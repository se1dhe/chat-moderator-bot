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
          <span className="badge badge-gold">PRO</span>
        </button>
      )}
      {r.locked && (
        <div className="card card-pad" style={{ display: 'flex', alignItems: 'center', gap: '0.7rem' }}>
          <span className="badge badge-danger"><Lock size={12} /> {t('raid.locked')}</span>
          <div className="header-spacer" />
          <button className="btn btn-danger" onClick={() => { haptic('warning'); s.updateSection('raid', { locked: false }) }}>
            {t('raid.unlock')}
          </button>
        </div>
      )}
      <div className="section-label">{t('sec.raid')}</div>
      <div className="card">
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
