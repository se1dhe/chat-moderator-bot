import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Shield, Users, Megaphone, ChevronRight, ServerCrash, Inbox } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { useLang } from '../context/LangContext'
import { api } from '../lib/api'
import { startParam, haptic } from '../lib/telegram'
import { Preloader } from '../components/Preloader'
import { GlobalOnboarding } from '../components/GlobalOnboarding'
import { ThemeToggle } from '../components/ThemeToggle'

const typeIcon = (type) => (type === 'channel' ? Megaphone : Users)

function ChatAvatar({ cid, type }) {
  const [error, setError] = useState(false)
  const Ico = typeIcon(type)
  if (error) return <Ico size={20} />
  return <img src={`/api/chats/${cid}/avatar`} onError={() => setError(true)} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
}

export function ChatPicker() {
  const { t, lang, setLang } = useLang()
  const navigate = useNavigate()
  const [state, setState] = useState({ loading: true })

  const load = () => {
    setState({ loading: true })
    api.me()
      .then((data) => {
        if (data.user?.lang && data.user.lang !== lang) {
          setLang(data.user.lang)
        }
        
        const sp = startParam()
        if (sp && data.chats.some((c) => String(c.id) === sp)) {
          navigate(`/c/${sp}`, { replace: true })
          return
        }
        setTimeout(() => setState({ loading: false, data }), 800)
      })
      .catch((e) => setState({ loading: false, error: e }))
  }

  useEffect(() => {
    load()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [navigate])

  const cycle = { en: 'ru', ru: 'uk', uk: 'en' }

  return (
    <>
      <AnimatePresence>
        {state.loading && <Preloader key="preloader" />}
      </AnimatePresence>

      {!state.loading && (
        <motion.div 
          className="shell"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, ease: 'easeOut' }}
        >
      <header className="app-header">
        <div className="logo" style={{ overflow: 'hidden', padding: 0, background: 'none' }}>
          <img src="/app/logo.jpg" alt="Logo" style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: 'inherit' }} />
        </div>
        <div>
          <div className="title">{t('app.title')}</div>
          <div className="subtitle">{t('app.subtitle')}</div>
        </div>
        <div className="header-spacer" />
        <button className="lang-toggle" onClick={() => { haptic('light'); setLang(cycle[lang]) }}>{lang}</button>
        <ThemeToggle />
      </header>

      <div className="content no-nav">
        {state.error ? (
          <div className="center-state">
            <ServerCrash size={44} className="ico" />
            <h3>{t('common.error')}</h3>
            <button className="btn" onClick={() => load()}>
              {t('common.retry')}
            </button>
          </div>
        ) : !state.data.chats.length ? (
          <GlobalOnboarding botUsername={state.data.bot?.username} />
        ) : (
          <>
            <div className="section-label">{t('chats.subtitle')}</div>
            {state.data.chats.map((c) => {
              return (
                <button key={c.id} className="tile fade-in" onClick={() => { haptic('light'); navigate(`/c/${c.id}`) }}>
                  <div className="tile-icon" style={{ overflow: 'hidden', padding: 0 }}><ChatAvatar cid={c.id} type={c.type} /></div>
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
        </motion.div>
      )}
    </>
  )
}
