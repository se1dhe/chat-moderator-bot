import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ShieldAlert, ShieldBan, Shield } from 'lucide-react';
import { useLang } from '../context/LangContext';
import { API_BASE } from '../lib/api';
import { initData } from '../lib/telegram';

interface FeedEvent {
  id: number | string;
  action: string;
  user_name: string;
  chat_title: string;
  reason?: string;
}

export function LiveFeed({ standalone = false }: { standalone?: boolean }) {
  const [events, setEvents] = useState<FeedEvent[]>([]);
  const { t } = useLang();

  useEffect(() => {
    // connect to SSE with auth token as query parameter
    const evtSource = new EventSource(`${API_BASE}/live/feed?initData=${encodeURIComponent(initData)}`);
    
    evtSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setEvents(prev => {
          const next = [{ ...data, id: Date.now() + Math.random() }, ...prev];
          return next.slice(0, 8); // keep last 8 events
        });
      } catch (e) {
        // ignore parsing errors
      }
    };

    return () => evtSource.close();
  }, []);

  const getIcon = (action: string) => {
    switch (action) {
      case 'ban': return <ShieldBan size={18} className="text-red-500" />;
      case 'warn': return <ShieldAlert size={18} className="text-amber-500" />;
      default: return <Shield size={18} className="text-primary" />;
    }
  };

  const getActionText = (action: string) => {
    switch (action) {
      case 'ban': return t('live.banned');
      case 'warn': return t('live.warned');
      case 'mute': return t('live.muted');
      case 'kick': return t('live.kicked');
      case 'unban': return t('live.unbanned');
      default: return action;
    }
  };

  if (events.length === 0) {
    return (
      <div className={`flex flex-col items-center justify-center text-center opacity-70 p-6 ${standalone ? 'h-[400px]' : 'h-[280px]'}`}>
        <div className="w-8 h-8 rounded-full border-2 border-neutral-300 dark:border-neutral-700 border-t-neutral-400 dark:border-t-neutral-500 animate-spin mb-4" />
        <span className="text-neutral-500 font-medium">{t('live.waiting')}</span>
      </div>
    );
  }

  return (
    <div className={`relative overflow-hidden w-full ${standalone ? 'h-[400px]' : 'h-[360px] bg-white dark:bg-neutral-900 rounded-2xl border border-neutral-200 dark:border-neutral-800'}`}>
      <div className="absolute top-0 left-0 right-0 p-3 bg-white/90 dark:bg-neutral-900/90 backdrop-blur-md z-10 border-b border-neutral-200 dark:border-neutral-800 flex items-center gap-2 text-[13px] font-bold text-neutral-500 uppercase tracking-wider">
        <div className="w-2 h-2 rounded-full bg-red-500 shadow-[0_0_8px_#ef4444] animate-pulse" />
        {t('live.feedTitle')}
      </div>
      
      <div className="pt-14 p-3 flex flex-col gap-2 overflow-hidden h-full">
        <AnimatePresence>
          {events.map((ev) => (
            <motion.div
              key={ev.id}
              initial={{ opacity: 0, x: -20, scale: 0.95 }}
              animate={{ opacity: 1, x: 0, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              transition={{ type: "spring", stiffness: 400, damping: 25 }}
              className="flex items-start gap-3 p-3 bg-neutral-50 dark:bg-neutral-950 border border-neutral-200 dark:border-neutral-800 rounded-xl"
            >
              <div className="mt-0.5 shrink-0 bg-white dark:bg-neutral-900 p-2 rounded-full border border-neutral-200 dark:border-neutral-800 shadow-sm">
                {getIcon(ev.action)}
              </div>
              <div className="flex-1 min-w-0 flex flex-col">
                <div className="flex items-center justify-between gap-2 mb-0.5">
                  <span className="font-bold text-sm text-neutral-900 dark:text-neutral-50 truncate">
                    {ev.user_name}
                  </span>
                  <span className="text-[11px] font-medium text-neutral-400 shrink-0 truncate">
                    {t('live.inChat').replace('{chat}', ev.chat_title)}
                  </span>
                </div>
                <div className="text-[13px] text-neutral-500 flex items-center gap-1.5 flex-wrap">
                  <span className={`font-semibold ${ev.action === 'ban' ? 'text-red-500' : ev.action === 'warn' ? 'text-amber-500' : 'text-primary'}`}>
                    {getActionText(ev.action)}
                  </span>
                  {ev.reason && (
                    <>
                      <span className="text-neutral-300 dark:text-neutral-700">•</span>
                      <span className="truncate flex-1 min-w-0">{ev.reason}</span>
                    </>
                  )}
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
}
