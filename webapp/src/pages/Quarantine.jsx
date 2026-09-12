import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { ShieldCheck, Check, Ban, Ruler } from 'lucide-react'
import { useLang } from '../context/LangContext'
import { api } from '../lib/api'
import { Spinner } from '../components/ui'
import { haptic } from '../lib/telegram'

export function Quarantine() {
  const { cid } = useParams()
  const { t } = useLang()
  const [items, setItems] = useState(null)
  const [busy, setBusy] = useState(null)

  useEffect(() => {
    let alive = true
    api.quarantine(cid).then((d) => alive && setItems(d)).catch(() => alive && setItems([]))
    return () => { alive = false }
  }, [cid])

  const decide = async (vid, action) => {
    setBusy(vid)
    try {
      await api.decide(cid, vid, action)
      haptic(action === 'approve' ? 'success' : 'warning')
      setItems((list) => list.filter((v) => v.id !== vid))
    } catch (e) {
      haptic('error')
      window.Telegram?.WebApp?.showAlert?.(e.message || 'Error processing decision')
    } finally {
      setBusy(null)
    }
  }

  if (!items) return <div className="content"><Spinner /></div>

  if (!items.length) {
    return (
      <div className="content">
        <div className="center-state">
          <ShieldCheck size={44} className="ico" />
          <h3>{t('nav.quarantine')}</h3>
          <p>{t('quar.empty')}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="content fade-in">
      <div className="section-label">{t('quar.title')} · {items.length}</div>
      {items.map((v) => (
        <div key={v.id} className="card q-card">
          <div className="q-head">
            <span className="q-cat">{t(`cat.${v.category}`) || v.category}</span>
            <span className="badge badge-gold">{v.score}% {t('quar.confidence')}</span>
          </div>
          <div className="q-reason">{t('quar.from')}: <code>{v.user_id}</code></div>
          {v.text && <div className="q-text">{v.text}</div>}
          {v.explanation && <div className="q-reason">{v.explanation}</div>}
          <div className="q-actions">
            <button className="btn btn-success" disabled={busy === v.id} onClick={() => decide(v.id, 'approve')}>
              <Check size={15} /> {t('quar.approve')}
            </button>
            <button className="btn btn-danger" disabled={busy === v.id} onClick={() => decide(v.id, 'ban')}>
              <Ban size={15} /> {t('quar.ban')}
            </button>
            <button className="btn" disabled={busy === v.id} onClick={() => decide(v.id, 'rule')}>
              <Ruler size={15} /> {t('quar.rule')}
            </button>
          </div>
        </div>
      ))}
    </div>
  )
}
