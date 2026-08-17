import { useState } from 'react'
import { Crown, Sparkles } from 'lucide-react'
import { useLang } from '../context/LangContext'
import { useChatSettings } from '../context/ChatSettingsContext'

const fmtDate = (iso) => (iso ? new Date(iso).toLocaleDateString() : '')

export function ProBanner() {
  const { t } = useLang()
  const { billing, pro, openUpgrade } = useChatSettings()
  const [busy, setBusy] = useState(false)

  if (!billing) return null

  if (pro) {
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
    try { await openUpgrade() } finally { setBusy(false) }
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
