import { useState } from 'react'

export default function Webhooks({ s, t }) {
  const url = s.draft.webhook_url || ''
  
  return (
    <>
      <div className="section-label">{t('sec.webhooks')}</div>
      <div className="card card-pad" style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
        <div className="row-desc">{t('webhooks.desc')}</div>
        <div style={{ fontWeight: 600, fontSize: '15px', marginTop: '0.5rem' }}>{t('webhooks.url')}</div>
        <input
          type="text"
          className="input"
          value={url}
          placeholder="https://example.com/webhook"
          onChange={(e) => s.setSection('webhook_url', e.target.value)}
        />
      </div>
    </>
  )
}
