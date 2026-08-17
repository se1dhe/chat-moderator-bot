import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { BarChart3, Lock, Sparkles } from 'lucide-react'
import { useLang } from '../context/LangContext'
import { useChatSettings } from '../context/ChatSettingsContext'
import { api } from '../lib/api'
import { Spinner } from '../components/ui'

// Build the last 14 UTC days, filling gaps from the sparse timeline map.
function last14(timeline) {
  const out = []
  const now = new Date()
  for (let i = 13; i >= 0; i--) {
    const d = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate() - i))
    const key = d.toISOString().slice(0, 10)
    out.push({ key, day: d.getUTCDate(), count: timeline[key] || 0 })
  }
  return out
}

export function Stats() {
  const { cid } = useParams()
  const { t } = useLang()
  const { pro, billing, openUpgrade } = useChatSettings()
  const [data, setData] = useState(null)

  useEffect(() => {
    if (!pro) return  // analytics is a Pro feature — don't fetch when locked
    let alive = true
    api.stats(cid).then((d) => alive && setData(d)).catch(() => alive && setData({ actions: {}, pending_quarantine: 0, timeline: {}, categories: {}, members: 0 }))
    return () => { alive = false }
  }, [cid, pro])

  // Wait for billing to resolve, then gate: analytics requires Pro.
  if (billing === null) return <div className="content"><Spinner /></div>
  if (!pro) {
    return (
      <div className="content fade-in">
        <div className="center-state">
          <div className="lock-hero"><Lock size={40} /></div>
          <h3>{t('stats.proTitle')}</h3>
          <p>{t('stats.proPitch')}</p>
          <button className="btn btn-primary" onClick={() => openUpgrade()}>
            <Sparkles size={16} /> {t('pro.upgrade')}
          </button>
        </div>
      </div>
    )
  }

  if (!data) return <div className="content"><Spinner /></div>

  const actions = Object.entries(data.actions).sort((a, b) => b[1] - a[1])
  const total = actions.reduce((n, [, v]) => n + v, 0)
  const maxAction = actions.length ? actions[0][1] : 1

  const days = last14(data.timeline || {})
  const maxDay = Math.max(1, ...days.map((d) => d.count))

  const cats = Object.entries(data.categories || {}).filter(([c]) => c !== 'ok').sort((a, b) => b[1] - a[1])
  const maxCat = cats.length ? cats[0][1] : 1

  return (
    <div className="content fade-in">
      <div className="section-label">{t('stats.title')}</div>
      <div className="stat-grid">
        <div className="stat"><div className="stat-num">{total}</div><div className="stat-label">{t('stats.total')}</div></div>
        <div className="stat"><div className="stat-num" style={{ color: data.pending_quarantine ? 'var(--primary-light)' : undefined }}>{data.pending_quarantine}</div><div className="stat-label">{t('stats.pending')}</div></div>
        <div className="stat"><div className="stat-num">{data.members || 0}</div><div className="stat-label">{t('stats.members')}</div></div>
        <div className="stat"><div className="stat-num">{cats.reduce((n, [, v]) => n + v, 0)}</div><div className="stat-label">{t('stats.categories')}</div></div>
      </div>

      <div className="section-label">{t('stats.last14')}</div>
      <div className="card card-pad">
        <div className="chart">
          {days.map((d) => (
            <div className="chart-col" key={d.key} title={`${d.key}: ${d.count}`}>
              <div className="chart-bar" style={{ height: `${(d.count / maxDay) * 100}%` }} />
              <div className="chart-x">{d.day}</div>
            </div>
          ))}
        </div>
      </div>

      {cats.length > 0 && (
        <>
          <div className="section-label">{t('stats.categories')}</div>
          <div className="card card-pad">
            {cats.map(([cat, n]) => (
              <div key={cat} className="bar-row">
                <span className="bar-label">{t(`cat.${cat}`) !== `cat.${cat}` ? t(`cat.${cat}`) : cat}</span>
                <span className="bar-track"><span className="bar-fill" style={{ width: `${(n / maxCat) * 100}%` }} /></span>
                <span className="bar-num">{n}</span>
              </div>
            ))}
          </div>
        </>
      )}

      {actions.length > 0 ? (
        <>
          <div className="section-label">{t('stats.actions')}</div>
          <div className="card card-pad">
            {actions.map(([action, n]) => (
              <div key={action} className="bar-row">
                <span className="bar-label">{action.replace(/_/g, ' ')}</span>
                <span className="bar-track"><span className="bar-fill" style={{ width: `${(n / maxAction) * 100}%` }} /></span>
                <span className="bar-num">{n}</span>
              </div>
            ))}
          </div>
        </>
      ) : (
        <div className="center-state"><BarChart3 size={44} className="ico" /><p>{t('stats.empty')}</p></div>
      )}
    </div>
  )
}
