import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Users, Megaphone, ChevronRight, ServerCrash } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useLang } from '../context/LangContext';
import { api } from '../lib/api';
import { startParam, haptic } from '../lib/telegram';
import { Preloader } from '../components/Preloader';
import { GlobalOnboarding } from '../components/GlobalOnboarding';
import { ThemeToggle } from '../components/ThemeToggle';
import { MeResponse } from '../lib/types';

const typeIcon = (type: string) => (type === 'channel' ? Megaphone : Users);

function ChatAvatar({ cid, type }: { cid: number; type: string }) {
  const [error, setError] = useState(false);
  const Ico = typeIcon(type);
  if (error) return <div className="w-full h-full flex items-center justify-center bg-neutral-100 dark:bg-neutral-800 text-neutral-500"><Ico size={20} /></div>;
  return <img src={`/api/chats/${cid}/avatar`} onError={() => setError(true)} className="w-full h-full object-cover" />;
}

export function ChatPicker() {
  const { t, lang, setLang } = useLang();
  const navigate = useNavigate();
  const [state, setState] = useState<{ loading: boolean; data?: MeResponse; error?: any }>({ loading: true });

  const load = () => {
    setState({ loading: true });
    api.me()
      .then((data) => {
        if (data.user?.lang && data.user.lang !== lang) {
          setLang(data.user.lang);
        }
        
        const sp = startParam();
        if (sp && data.chats.some((c) => String(c.id) === sp)) {
          navigate(`/c/${sp}`, { replace: true });
          return;
        }
        setTimeout(() => setState({ loading: false, data }), 800);
      })
      .catch((error) => setState({ loading: false, error }));
  };

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [navigate]);

  const cycle: Record<string, string> = { en: 'ru', ru: 'uk', uk: 'en' };

  return (
    <>
      <AnimatePresence>
        {state.loading && <Preloader key="preloader" />}
      </AnimatePresence>

      {!state.loading && (
        <motion.div 
          className="w-full max-w-md mx-auto min-h-screen flex flex-col bg-neutral-50 dark:bg-neutral-950 text-neutral-900 dark:text-neutral-50"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, ease: 'easeOut' }}
        >
          <header className="sticky top-0 z-40 w-full flex items-center h-16 px-4 bg-white/80 dark:bg-neutral-900/80 backdrop-blur-md border-b border-neutral-200 dark:border-neutral-800">
            <div className="w-10 h-10 rounded-full overflow-hidden shrink-0 border border-neutral-200 dark:border-neutral-800 mr-3">
              <img src="/app/logo.jpg" alt="Logo" className="w-full h-full object-cover" />
            </div>
            
            <div className="flex-1 min-w-0">
              <h1 className="text-lg font-bold truncate text-neutral-900 dark:text-neutral-50 tracking-tight leading-tight">
                {t('app.title')}
              </h1>
              <p className="text-xs text-neutral-500 truncate">{t('app.subtitle')}</p>
            </div>

            <div className="flex items-center gap-2 shrink-0 ml-2">
              <button 
                className="text-xs font-bold uppercase tracking-wider px-2 py-1 bg-neutral-100 dark:bg-neutral-800 text-neutral-600 dark:text-neutral-300 rounded-md hover:bg-neutral-200 dark:hover:bg-neutral-700 transition-colors"
                onClick={() => { haptic('light'); setLang(cycle[lang]); }}
              >
                {lang}
              </button>
              <ThemeToggle />
            </div>
          </header>

          <main className="flex-1 w-full px-4 py-6 pb-12 flex flex-col">
            {state.error ? (
              <div className="flex-1 flex flex-col items-center justify-center text-center gap-4 py-12 text-neutral-500">
                <ServerCrash size={48} className="text-primary" />
                <h3 className="font-semibold text-neutral-800 dark:text-neutral-200">{t('common.error')}</h3>
                <button 
                  className="px-6 py-2.5 bg-neutral-200 dark:bg-neutral-800 hover:bg-neutral-300 dark:hover:bg-neutral-700 rounded-xl font-medium transition-colors mt-2" 
                  onClick={() => load()}
                >
                  {t('common.retry')}
                </button>
              </div>
            ) : !state.data?.chats.length ? (
              <GlobalOnboarding botUsername={state.data?.bot?.username} />
            ) : (
              <div className="w-full flex flex-col gap-3">
                <h2 className="text-sm font-semibold text-neutral-500 uppercase tracking-wider mb-1 ml-1">{t('chats.subtitle')}</h2>
                {state.data.chats.map((c, i) => (
                  <motion.button 
                    key={c.id} 
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.05 }}
                    className="w-full flex items-center p-4 bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-2xl shadow-sm hover:border-primary/30 dark:hover:border-primary/30 active:scale-[0.98] transition-all text-left" 
                    onClick={() => { haptic('light'); navigate(`/c/${c.id}`); }}
                  >
                    <div className="w-12 h-12 rounded-full overflow-hidden shrink-0 border border-neutral-100 dark:border-neutral-800 mr-4">
                      <ChatAvatar cid={c.id} type={c.type} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="font-bold text-neutral-900 dark:text-neutral-50 truncate text-base leading-tight">
                        {c.title || `#${c.id}`}
                      </div>
                      <div className="text-sm text-neutral-500 mt-0.5">
                        {t(`chats.${c.type}`)}
                      </div>
                    </div>
                    <ChevronRight size={20} className="text-neutral-400 shrink-0 ml-2" />
                  </motion.button>
                ))}
              </div>
            )}
          </main>
        </motion.div>
      )}
    </>
  );
}
