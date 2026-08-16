import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { BarChart3 } from 'lucide-react'
import { useLang } from '../context/LangContext'
import { api } from '../lib/api'
import { Spinner } from '../components/ui'

export function Stats() {
  const { cid } = useParams()
  const { t } = useLang()
  const [data, setData] = useState(null)

  useEffect(() => {
    let alive = true
    api.stats(cid).then((d) => alive && setData(d)).catch(() => alive && setData({ actions: {}, pending_quarantine: 0 }))
    return () => { alive = false }
  }, [cid])

  if (!data) return <div className="content"><Spinner /></div>

  const entries = Object.entries(data.actions).sort((a, b) => b[1] - a[1])
  const total = entries.reduce((n, [, v]) => n + v, 0)
  const max = entries.length ? entries[0][1] : 1

  return (
    <div className="content fade-in">
      <div className="section-label">{t('stats.title')}</div>
      <div className="stat-grid">
        <div className="stat">
          <div className="stat-num">{total}</div>
          <div className="stat-label">{t('stats.total')}</div>
        </div>
        <div className="stat">
          <div className="stat-num" style={{ color: data.pending_quarantine ? 'var(--primary-light)' : undefined }}>
            {data.pending_quarantine}
          </div>
          <div className="stat-label">{t('stats.pending')}</div>
        </div>
      </div>

      {entries.length ? (
        <>
          <div className="section-label">{t('stats.actions')}</div>
          <div className="card card-pad">
            {entries.map(([action, n]) => (
              <div key={action} className="bar-row">
                <span className="bar-label">{action.replace(/_/g, ' ')}</span>
                <span className="bar-track"><span className="bar-fill" style={{ width: `${(n / max) * 100}%` }} /></span>
                <span className="bar-num">{n}</span>
              </div>
            ))}
          </div>
        </>
      ) : (
        <div className="center-state">
          <BarChart3 size={44} className="ico" />
          <p>{t('stats.empty')}</p>
        </div>
      )}
    </div>
  )
}
