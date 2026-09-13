import { useState, useEffect, useRef } from 'react'
import { Plus, Lock } from 'lucide-react'
import { Toggle, Row, Segmented, Stepper, Slider, Chips, Spinner } from '../../components/ui'
import { haptic, showAlert } from '../../lib/telegram'
import { api } from '../../lib/api'

export default function Welcome({ s, t }) {
  const msg = s.draft.onboarding?.welcome_message || ''
  return (
    <>
      <div className="section-label">{t('sec.welcome')}</div>
      <div className="card card-pad" style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
        <div className="row-desc">{t('welcome.desc')}</div>
        <div style={{ fontWeight: 600, fontSize: '15px', marginTop: '0.5rem' }}>{t('welcome.text')}</div>
        <textarea
          className="input"
          style={{ minHeight: '120px', resize: 'vertical' }}
          value={msg}
          placeholder={t('welcome.text.ph')}
          onChange={(e) => s.updateSection('onboarding', { welcome_message: e.target.value })}
        ></textarea>
      </div>
    </>
  )
}
