import { NavLink, useNavigate, useParams, useLocation, useOutlet } from 'react-router-dom';
import { LayoutGrid, Users, ShieldAlert, ScrollText, BarChart3, ChevronLeft, Check, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useLang } from '../context/LangContext';
import { ChatSettingsProvider, useChatSettings } from '../context/ChatSettingsContext';
import { haptic, isTelegram } from '../lib/telegram';
import { ThemeToggle } from './ThemeToggle';

function SaveHint() {
  const { saving } = useChatSettings();
  const { t } = useLang();
  return (
    <span className={`flex items-center gap-1.5 text-xs font-medium px-2 py-1 rounded-full transition-colors ${
      saving ? 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400' : 'text-emerald-600 dark:text-emerald-400'
    }`}>
      {saving ? <Loader2 size={12} className="animate-spin" /> : <Check size={12} />}
      {saving ? t('common.saving') : t('common.saved')}
    </span>
  );
}

function Header() {
  const { t, lang, setLang } = useLang();
  const navigate = useNavigate();
  const { section } = useParams();
  const cycle: Record<string, string> = { en: 'ru', ru: 'uk', uk: 'en' };

  return (
    <header className="sticky top-0 z-40 w-full flex items-center h-14 px-4 bg-white/80 dark:bg-black/70 backdrop-blur-xl border-b border-neutral-200 dark:border-neutral-800/60">
      {section && !isTelegram ? (
        <button 
          className="p-2 -ml-2 text-neutral-900 dark:text-neutral-50 hover:bg-neutral-100 dark:hover:bg-neutral-800 rounded-full transition-colors"
          onClick={() => { haptic('light'); navigate(-1); }}
        >
          <ChevronLeft size={24} />
        </button>
      ) : (
        <div className="w-8 h-8 rounded-full overflow-hidden shrink-0 border border-neutral-200 dark:border-neutral-800/60 mr-3">
          <img src="/app/logo.jpg" alt="Logo" className="w-full h-full object-cover" />
        </div>
      )}
      
      <div className="flex-1 min-w-0">
        <h1 className="text-lg font-bold truncate text-neutral-900 dark:text-white tracking-tight dark:drop-shadow-[0_2px_10px_rgba(0,0,0,1)]">
          {t('app.title')}
        </h1>
      </div>

      <div className="flex items-center gap-2 shrink-0 ml-2">
        {section && <SaveHint />}
        <button 
          className="text-xs font-bold uppercase tracking-wider px-2 py-1 bg-neutral-100 dark:bg-neutral-800 text-neutral-600 dark:text-neutral-300 rounded-md hover:bg-neutral-200 dark:hover:bg-neutral-700 transition-colors"
          onClick={() => { haptic('light'); setLang(cycle[lang]); }}
        >
          {lang}
        </button>
        <ThemeToggle />
      </div>
    </header>
  );
}

function Nav({ cid }: { cid: string }) {
  const { t } = useLang();
  const base = `/c/${cid}`;
  const items = [
    { to: base, icon: LayoutGrid, label: t('nav.dashboard'), end: true },
    { to: `${base}/members`, icon: Users, label: t('nav.members') },
    { to: `${base}/quarantine`, icon: ShieldAlert, label: t('nav.quarantine') },
    { to: `${base}/audit`, icon: ScrollText, label: t('nav.audit') },
    { to: `${base}/stats`, icon: BarChart3, label: t('nav.stats') },
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-40 bg-white/90 dark:bg-black/80 backdrop-blur-2xl border-t border-neutral-200 dark:border-neutral-800/60 pb-safe">
      <div className="max-w-md mx-auto w-full flex items-center justify-between px-2 h-16">
        {items.map((it) => (
          <NavLink 
            key={it.to} 
            to={it.to} 
            end={it.end} 
            onClick={() => haptic('light')}
            className={({ isActive }) => `
              flex flex-col items-center justify-center w-full h-full gap-1 transition-colors
              ${isActive ? 'text-primary' : 'text-neutral-500 hover:text-neutral-900 dark:hover:text-neutral-300'}
            `}
          >
            {({ isActive }) => (
              <>
                <it.icon size={22} className={isActive ? 'fill-primary/10' : ''} />
                <span className="text-[10px] font-medium leading-none">{it.label}</span>
              </>
            )}
          </NavLink>
        ))}
      </div>
    </nav>
  );
}

export function Layout() {
  const { cid } = useParams<{ cid: string }>();
  const location = useLocation();
  const outlet = useOutlet();
  
  if (!cid) return null;

  return (
    <ChatSettingsProvider chatId={Number(cid)}>
      <div className="w-full max-w-md mx-auto min-h-screen flex flex-col bg-neutral-50 dark:bg-black text-neutral-900 dark:text-neutral-50 relative">
        <Header />
        
        <main className="flex-1 w-full  pb-24 pt-4 px-4 flex flex-col relative">
          {outlet}
        </main>

        <Nav cid={cid} />
      </div>
    </ChatSettingsProvider>
  );
}
