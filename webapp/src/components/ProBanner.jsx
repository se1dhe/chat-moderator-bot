import { useEffect, useState } from 'react'
import { Crown, Sparkles } from 'lucide-react'
import { useLang } from '../context/LangContext'
import { api } from '../lib/api'
import { openInvoice, haptic } from '../lib/telegram'

const fmtDate = (iso) => (iso ? new Date(iso).toLocaleDateString() : '')

export function ProBanner({ chatId }) {
  const { t } = useLang()
  const [billing, setBilling] = useState(null)
  const [busy, setBusy] = useState(false)

  const load = () => api.billing(chatId).then(setBilling).catch(() => setBilling(null))
  useEffect(() => { load() /* eslint-disable-next-line */ }, [chatId])

  if (!billing) return null

  if (billing.pro) {
    return (
      <div className="pro-banner pro-banner--active">
        <Crown size={20} />
        <div className="pro-banner-body">
          <div className="pro-banner-title">{t('pro.active')}</div>
          <div className="pro-banner-sub">{t('pro.until', { date: fmtDate(billing.active_until) })}</div>
        </div>
        <span className="badge badge-gold">{t('pro.badge')}</span>
      </div>
    )
  }

  const upgrade = async () => {
    setBusy(true)
    haptic('light')
    try {
      const { url } = await api.invoice(chatId)
      const status = await openInvoice(url)
      if (status === 'paid') {
        haptic('success')
        await load()
      }
    } finally {
      setBusy(false)
    }
  }

  return (
    <button className="pro-banner pro-banner--cta" onClick={upgrade} disabled={busy}>
      <Sparkles size={20} />
      <div className="pro-banner-body">
        <div className="pro-banner-title">{busy ? t('pro.opening') : t('pro.upgrade')}</div>
        <div className="pro-banner-sub">{t('pro.pitch')}</div>
      </div>
      <span className="pro-price">{t('pro.price', { stars: billing.price_stars, days: billing.period_days })}</span>
    </button>
  )
}
