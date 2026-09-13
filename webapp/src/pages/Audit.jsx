import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { ScrollText } from 'lucide-react'
import { useLang } from '../context/LangContext'
import { api } from '../lib/api'
import { Spinner } from '../components/ui'

const fmt = (iso) => {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

export function Audit() {
  const { cid } = useParams()
  const { t } = useLang()
  const [rows, setRows] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    let alive = true
    api.audit(cid, 100)
      .then((d) => alive && setRows(d))
      .catch((err) => {
        if (alive) {
          setError(err.message)
          setRows([]) // keep it as empty so it stops spinning, but we have error state
        }
      })
    return () => { alive = false }
  }, [cid])

  if (!rows && !error) return <div className="content"><Spinner /></div>

  if (error) {
    return (
      <div className="content fade-in">
        <div className="center-state">
          <div style={{ color: '#ef4444', marginBottom: 16 }}>{error}</div>
          <button className="btn btn-secondary" onClick={() => { setError(null); setRows(null); api.audit(cid, 100).then(setRows).catch(e => setError(e.message)) }}>Retry</button>
        </div>
      </div>
    )
  }

  if (!rows.length) {
    return (
      <div className="content">
        <div className="center-state">
          <ScrollText size={44} className="ico" />
          <h3>{t('audit.title')}</h3>
          <p>{t('audit.empty')}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="content fade-in">
      <div className="section-label">{t('audit.title')}</div>
      <div className="card">
        {rows.map((r) => (
          <div key={r.id} className="audit-item">
            <div className={`audit-dot ${r.action}`} />
            <div className="audit-body">
              <div className="audit-action">{r.action.replace(/_/g, ' ')}</div>
              <div className="audit-meta">
                {r.user_id ? `user ${r.user_id}` : ''}{r.reason ? ` · ${r.reason}` : ''}
              </div>
            </div>
            <div className="audit-meta">{fmt(r.created_at)}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
