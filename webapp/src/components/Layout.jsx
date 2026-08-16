import { NavLink, Outlet, useNavigate, useParams } from 'react-router-dom'
import { LayoutGrid, ShieldAlert, ScrollText, BarChart3, ChevronLeft, Shield } from 'lucide-react'
import { useLang } from '../context/LangContext'
import { ChatSettingsProvider, useChatSettings } from '../context/ChatSettingsContext'
import { haptic } from '../lib/telegram'

function SaveBar() {
  const { dirty, saving, save, reset } = useChatSettings()
  const { t } = useLang()
  return (
    <div className={`savebar ${dirty ? 'show' : ''}`}>
      <div style={{ display: 'flex', gap: '0.6rem' }}>
        <button className="btn btn-ghost" onClick={reset} disabled={saving}>{t('common.cancel')}</button>
        <button className="btn btn-primary btn-block" onClick={save} disabled={saving}>
          {saving ? t('common.saving') : t('common.save')}
        </button>
      </div>
    </div>
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
        <div className="logo"><Shield size={19} /></div>
      )}
      <div>
        <div className="title">{t('app.title')}</div>
        <div className="subtitle">{t('app.subtitle')}</div>
      </div>
      <div className="header-spacer" />
      <button className="lang-toggle" onClick={() => { haptic('light'); setLang(cycle[lang]) }}>{lang}</button>
    </header>
  )
}

function Nav({ cid }) {
  const { t } = useLang()
  const base = `/c/${cid}`
  const items = [
    { to: base, icon: LayoutGrid, label: t('nav.dashboard'), end: true },
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
        <SaveBar />
      </div>
    </ChatSettingsProvider>
  )
}
