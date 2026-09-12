import { NavLink, Outlet, useNavigate, useParams } from 'react-router-dom'
import { LayoutGrid, Users, ShieldAlert, ScrollText, BarChart3, ChevronLeft, Shield, Check, Loader2 } from 'lucide-react'
import { useLang } from '../context/LangContext'
import { ChatSettingsProvider, useChatSettings } from '../context/ChatSettingsContext'
import { haptic } from '../lib/telegram'
import { WhatsNewModal } from './WhatsNewModal'

// Tiny in-flow autosave hint (no fixed bar → no scroll repaint glitch).
function SaveHint() {
  const { saving } = useChatSettings()
  const { t } = useLang()
  return (
    <span className={`save-hint ${saving ? 'is-saving' : ''}`}>
      {saving ? <Loader2 size={13} className="spin" /> : <Check size={13} />}
      {saving ? t('common.saving') : t('common.saved')}
    </span>
  )
}

function Header() {
  const { t, lang, setLang } = useLang()
  const navigate = useNavigate()
  const { section } = useParams()
  const cycle = { en: 'ru', ru: 'uk', uk: 'en' }
  return (
    <header className="app-header">
      {section ? (
        <button className="header-back" onClick={() => { haptic('light'); navigate(-1) }}>
          <ChevronLeft size={20} />
        </button>
      ) : (
        <div className="logo" style={{ overflow: 'hidden', padding: 0, background: 'none' }}>
          <img src="/app/logo.jpg" alt="Logo" style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: 'inherit' }} />
        </div>
      )}
      <div>
        <div className="title">{t('app.title')}</div>
        <div className="subtitle">{t('app.subtitle')}</div>
      </div>
      <div className="header-spacer" />
      {section ? <SaveHint /> : null}
      <button className="lang-toggle" onClick={() => { haptic('light'); setLang(cycle[lang]) }}>{lang}</button>
    </header>
  )
}

function Nav({ cid }) {
  const { t } = useLang()
  const base = `/c/${cid}`
  const items = [
    { to: base, icon: LayoutGrid, label: t('nav.dashboard'), end: true },
    { to: `${base}/members`, icon: Users, label: t('nav.members') },
    { to: `${base}/quarantine`, icon: ShieldAlert, label: t('nav.quarantine') },
    { to: `${base}/audit`, icon: ScrollText, label: t('nav.audit') },
    { to: `${base}/stats`, icon: BarChart3, label: t('nav.stats') },
  ]
  return (
    <nav className="bottom-nav">
      {items.map((it) => (
        <NavLink key={it.to} to={it.to} end={it.end} onClick={() => haptic('light')}>
          <it.icon size={20} />
          {it.label}
        </NavLink>
      ))}
    </nav>
  )
}

export function Layout() {
  const { cid } = useParams()
  return (
    <ChatSettingsProvider chatId={cid}>
      <div className="shell">
        <Header />
        <Outlet />
        <Nav cid={cid} />
        <WhatsNewModal />
      </div>
    </ChatSettingsProvider>
  )
}
