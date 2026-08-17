import { useEffect, useState, useCallback } from 'react'
import { useParams } from 'react-router-dom'
import { Users, Search, TriangleAlert, VolumeX, Volume2, UserMinus, Ban, RotateCcw } from 'lucide-react'
import { useLang } from '../context/LangContext'
import { api } from '../lib/api'
import { Spinner } from '../components/ui'
import { haptic, showConfirm } from '../lib/telegram'

const ACTIONS = [
  { key: 'warn', icon: TriangleAlert, cls: '' },
  { key: 'mute', icon: VolumeX, cls: '', extra: { minutes: 60 } },
  { key: 'unmute', icon: Volume2, cls: '' },
  { key: 'kick', icon: UserMinus, cls: 'btn-danger', confirm: true },
  { key: 'ban', icon: Ban, cls: 'btn-danger', confirm: true },
  { key: 'unban', icon: RotateCcw, cls: '' },
]

const nameOf = (m) => m.full_name || (m.username ? `@${m.username}` : `#${m.user_id}`)

export function Members() {
  const { cid } = useParams()
  const { t } = useLang()
  const [q, setQ] = useState('')
  const [rows, setRows] = useState(null)
  const [busy, setBusy] = useState(null)
  const [reasons, setReasons] = useState({})

  const load = useCallback((query) => {
    api.members(cid, query).then(setRows).catch(() => setRows([]))
  }, [cid])

  useEffect(() => {
    const id = setTimeout(() => load(q), 250)  // debounce
    return () => clearTimeout(id)
  }, [q, load])

  const act = async (m, a) => {
    if (a.confirm) {
      const ok = await showConfirm(t('members.confirm', { action: t(`act.${a.key}`), name: nameOf(m) }))
      if (!ok) return
    }
    setBusy(`${m.user_id}:${a.key}`)
    haptic(a.cls ? 'warning' : 'light')
    try {
      const reason = (reasons[m.user_id] || '').trim()
      await api.memberAction(cid, m.user_id, a.key, { ...(a.extra || {}), reason })
      haptic('success')
    } catch {
      haptic('error')
    } finally {
      setBusy(null)
    }
  }

  return (
    <div className="content fade-in">
      <div className="search-box">
        <Search size={16} />
        <input className="search-input" value={q} placeholder={t('members.search')}
          onChange={(e) => setQ(e.target.value)} />
      </div>

      {rows === null ? (
        <Spinner />
      ) : rows.length === 0 ? (
        <div className="center-state">
          <Users size={44} className="ico" />
          <p>{t('members.empty')}</p>
        </div>
      ) : (
        rows.map((m) => (
          <div key={m.user_id} className="card member-card">
            <div className="member-head">
              <div className="member-body">
                <div className="member-name">{nameOf(m)}</div>
                <div className="member-meta">
                  {m.username ? `@${m.username} · ` : ''}<code>{m.user_id}</code> · {t('members.messages', { n: m.message_count })}
                </div>
              </div>
            </div>
            <input
              className="input member-reason"
              value={reasons[m.user_id] || ''}
              placeholder={t('members.reason')}
              onChange={(e) => setReasons((r) => ({ ...r, [m.user_id]: e.target.value }))}
            />
            <div className="member-actions">
              {ACTIONS.map((a) => (
                <button key={a.key} className={`btn ${a.cls}`} disabled={busy === `${m.user_id}:${a.key}`}
                  onClick={() => act(m, a)}>
                  <a.icon size={14} /> {t(`act.${a.key}`)}
                </button>
              ))}
            </div>
          </div>
        ))
      )}
    </div>
  )
}
