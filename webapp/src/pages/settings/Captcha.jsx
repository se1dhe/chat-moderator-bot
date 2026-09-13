import { useState, useEffect, useRef } from 'react'
import { Plus, Lock } from 'lucide-react'
import { Toggle, Row, Segmented, Stepper, Slider, Chips, Spinner } from '../../components/ui'
import { haptic, showAlert } from '../../lib/telegram'
import { api } from '../../lib/api'

const mins = (sec) => Math.round(sec / 60)

export default function Captcha({ s, t }) {
  const c = s.draft.captcha
  return (
    <>
      <div className="section-label">{t('sec.captcha')}</div>
      <div className="card">
        <Row title={t('captcha.enabled')}>
          <Toggle checked={c.enabled} onChange={(v) => s.updateSection('captcha', { enabled: v })} />
        </Row>
        <Row title={t('captcha.timeout')} value={`${mins(c.timeout_seconds)} ${t('common.minutes')}`}>
          <Stepper value={mins(c.timeout_seconds)} min={1} max={30}
            onChange={(v) => s.updateSection('captcha', { timeout_seconds: v * 60 })} />
        </Row>
      </div>
      <div className="section-label">{t('captcha.mode')}</div>
      <Segmented
        value={c.mode}
        onChange={(v) => s.updateSection('captcha', { mode: v })}
        options={[
          { value: 'button', label: t('captcha.mode.button') },
          { value: 'math', label: t('captcha.mode.math') },
        ]}
      />
    </>
  )
}
