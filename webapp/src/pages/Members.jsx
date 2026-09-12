import { useEffect, useState, useCallback, useRef } from 'react'
import { useParams } from 'react-router-dom'
import { Users, Search, TriangleAlert, VolumeX, Volume2, UserMinus, Ban, RotateCcw } from 'lucide-react'
import { useLang } from '../context/LangContext'
import { api } from '../lib/api'
import { Spinner } from '../components/ui'
import { haptic, showConfirm } from '../lib/telegram'

// Action metadata. `duration: true` means the action takes a length (mute/ban).
const META = {
  warn: { icon: TriangleAlert, cls: '' },
  mute: { icon: VolumeX, cls: '', duration: true },
  unmute: { icon: Volume2, cls: '' },
  kick: { icon: UserMinus, cls: 'btn-danger', confirm: true },
  ban: { icon: Ban, cls: 'btn-danger', confirm: true, duration: true },
  unban: { icon: RotateCcw, cls: '' },
}

// Only offer actions that make sense for the member's current state, so you can't
// "unban" someone who isn't banned or "unmute" someone who isn't muted.
const actionsFor = (state) => {
  if (state === 'banned') return ['unban']
  if (state === 'muted') return ['warn', 'unmute', 'kick', 'ban']
  return ['warn', 'mute', 'kick', 'ban']
}

// minutes: 0 == permanent
const DURATIONS = [
  { key: '1h', minutes: 60 },
  { key: '8h', minutes: 480 },
  { key: '1d', minutes: 1440 },
  { key: '7d', minutes: 10080 },
  { key: 'perm', minutes: 0 },
]

const nameOf = (m) => m.full_name || (m.username ? `@${m.username}` : `#${m.user_id}`)

export function Members() {
  const { cid } = useParams()
  const { t } = useLang()
  const [q, setQ] = useState('')
  const [rows, setRows] = useState(null)
  const [busy, setBusy] = useState(null)
  const [reasons, setReasons] = useState({})
  const [durs, setDurs] = useState({})  // user_id -> minutes for mute/ban
  
  const abortCtrlRef = useRef(null)

  const load = useCallback((query) => {
    if (abortCtrlRef.current) abortCtrlRef.current.abort()
    const ctrl = new AbortController()
    abortCtrlRef.current = ctrl
    
    api.members(cid, query, { signal: ctrl.signal })
      .then(setRows)
      .catch((e) => {
        if (e.name !== 'AbortError') setRows([])
      })
  }, [cid])

  useEffect(() => {
    const id = setTimeout(() => load(q), 250)  // debounce
    return () => clearTimeout(id)
  }, [q, load])

  const act = async (m, key) => {
    const meta = META[key]
    if (meta.confirm) {
      const ok = await showConfirm(t('members.confirm', { action: t(`act.${key}`), name: nameOf(m) }))
      if (!ok) return
    }
    setBusy(`${m.user_id}:${key}`)
    haptic(meta.cls ? 'warning' : 'light')
    try {
      const reason = (reasons[m.user_id] || '').trim()
      const extra = meta.duration ? { minutes: durs[m.user_id] ?? 60 } : {}
      await api.memberAction(cid, m.user_id, key, { ...extra, reason })
      haptic('success')
      load(q)  // refresh so the member's state (and available actions) update
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
        rows.map((m) => {
          const acts = actionsFor(m.state)
          const showDuration = acts.some((k) => META[k].duration)
          const sel = durs[m.user_id] ?? 60
          return (
            <div key={m.user_id} className="card member-card">
              <div className="member-head">
                <div className="member-body">
                  <div className="member-name">
                    {nameOf(m)}
                    {m.state === 'banned' && <span className="badge badge-danger member-state">{t('members.banned')}</span>}
                    {m.state === 'muted' && <span className="badge badge-muted member-state">{t('members.muted')}</span>}
                  </div>
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
              {showDuration && (
                <div className="dur-picker">
                  <span className="dur-label">{t('members.duration')}</span>
                  <div className="dur-chips">
                    {DURATIONS.map((d) => (
                      <button key={d.key}
                        className={`dur-chip ${sel === d.minutes ? 'active' : ''}`}
                        onClick={() => { haptic('light'); setDurs((r) => ({ ...r, [m.user_id]: d.minutes })) }}>
                        {t(`dur.${d.key}`)}
                      </button>
                    ))}
                  </div>
                </div>
              )}
              <div className="member-actions">
                {acts.map((key) => {
                  const Icon = META[key].icon
                  return (
                    <button key={key} className={`btn ${META[key].cls}`} disabled={busy === `${m.user_id}:${key}`}
                      onClick={() => act(m, key)}>
                      <Icon size={14} /> {t(`act.${key}`)}
                    </button>
                  )
                })}
              </div>
            </div>
          )
        })
      )}
    </div>
  )
}
