import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Shield, Users, Megaphone, ChevronRight, ServerCrash, Inbox } from 'lucide-react'
import { useLang } from '../context/LangContext'
import { api } from '../lib/api'
import { startParam, haptic } from '../lib/telegram'
import { Spinner } from '../components/ui'

const typeIcon = (type) => (type === 'channel' ? Megaphone : Users)

export function ChatPicker() {
  const { t, lang, setLang } = useLang()
  const navigate = useNavigate()
  const [state, setState] = useState({ loading: true })

  useEffect(() => {
    let alive = true
    api.me()
      .then((data) => {
        if (!alive) return
        // Deep-linked straight to one chat → skip the picker.
        const sp = startParam()
        if (sp && data.chats.some((c) => String(c.id) === sp)) {
          navigate(`/c/${sp}`, { replace: true })
          return
        }
        setState({ loading: false, data })
      })
      .catch((e) => alive && setState({ loading: false, error: e }))
    return () => { alive = false }
  }, [navigate])

  if (state.loading) return <div className="shell"><Spinner /></div>

  const cycle = { en: 'ru', ru: 'uk', uk: 'en' }

  return (
    <div className="shell">
      <header className="app-header">
        <div className="logo" style={{ overflow: 'hidden', padding: 0, background: 'none' }}>
          <img src="/logo.jpg" alt="Logo" style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: 'inherit' }} />
        </div>
        <div>
          <div className="title">{t('app.title')}</div>
          <div className="subtitle">{t('app.subtitle')}</div>
        </div>
        <div className="header-spacer" />
        <button className="lang-toggle" onClick={() => { haptic('light'); setLang(cycle[lang]) }}>{lang}</button>
      </header>

      <div className="content no-nav">
        {state.error ? (
          <div className="center-state">
            <ServerCrash size={44} className="ico" />
            <h3>{t('common.error')}</h3>
            <button className="btn" onClick={() => setState({ loading: true }) || location.reload()}>
              {t('common.retry')}
            </button>
          </div>
        ) : !state.data.chats.length ? (
          <div className="center-state">
            <Inbox size={44} className="ico" />
            <h3>{t('chats.title')}</h3>
            <p>{t('chats.empty')}</p>
          </div>
        ) : (
          <>
            <div className="section-label">{t('chats.subtitle')}</div>
            {state.data.chats.map((c) => {
              const Ico = typeIcon(c.type)
              return (
                <button key={c.id} className="tile fade-in" onClick={() => { haptic('light'); navigate(`/c/${c.id}`) }}>
                  <div className="tile-icon"><Ico size={20} /></div>
                  <div className="tile-body">
                    <div className="tile-title">{c.title || `#${c.id}`}</div>
                    <div className="tile-desc">{t(`chats.${c.type}`)}</div>
                  </div>
                  <ChevronRight size={18} className="tile-chevron" />
                </button>
              )
            })}
          </>
        )}
      </div>
    </div>
  )
}
