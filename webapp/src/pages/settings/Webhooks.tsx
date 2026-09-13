import { useState } from 'react'

export default function Webhooks({ s, t }) {
  const url = s.draft.webhook_url || ''
  
  return (
    <>
      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('sec.webhooks')}</div>
      <div className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-2xl p-4 mb-4 shadow-sm w-full" style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
        <div className="row-desc">{t('webhooks.desc')}</div>
        <div style={{ fontWeight: 600, fontSize: '15px', marginTop: '0.5rem' }}>{t('webhooks.url')}</div>
        <input
          type="text"
          className="w-full px-4 py-3 bg-neutral-50 dark:bg-neutral-950 border border-neutral-200 dark:border-neutral-800 rounded-xl focus:outline-none focus:border-primary/50 transition-colors font-medium text-[15px]"
          value={url}
          placeholder="https://example.com/webhook"
          onChange={(e) => s.setSection('webhook_url', e.target.value)}
        />
      </div>
    </>
  )
}
