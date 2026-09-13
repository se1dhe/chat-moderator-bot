import { useState } from 'react'

export default function Webhooks({ s, t }) {
  const url = s.draft.webhook_url || ''
  
  return (
    <>
      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('sec.webhooks')}</div>
      <div className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-2xl p-4 mb-4 shadow-sm w-full flex flex-col gap-3">
        <div className="text-[13px] text-neutral-500 leading-snug">{t('webhooks.desc')}</div>
        <div className="mt-2 font-semibold text-[15px]">{t('webhooks.url')}</div>
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
