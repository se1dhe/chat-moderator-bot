import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ShieldAlert, ShieldBan, Shield } from 'lucide-react';
import { useLang } from '../context/LangContext';

export function LiveFeed() {
  const [events, setEvents] = useState([]);
  const { t } = useLang();

  useEffect(() => {
    // connect to SSE
    const evtSource = new EventSource("/api/live/feed");
    
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

  const getIcon = (action) => {
    switch (action) {
      case 'ban': return <ShieldBan size={18} className="text-red-500" />;
      case 'warn': return <ShieldAlert size={18} className="text-yellow-500" />;
      default: return <Shield size={18} className="text-primary" />;
    }
  };

  const getActionText = (action) => {
    switch (action) {
      case 'ban': return 'Banned';
      case 'warn': return 'Warned';
      case 'mute': return 'Muted';
      case 'kick': return 'Kicked';
      case 'unban': return 'Unbanned';
      default: return action;
    }
  };

  if (events.length === 0) {
    return (
      <div className="card p-6 text-center opacity-70" style={{ height: '280px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div className="flex flex-col items-center gap-3">
          <div className="spinner border-2" style={{ width: '24px', height: '24px', opacity: 0.5 }} />
          <span>Waiting for live events...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="card" style={{ height: '360px', overflow: 'hidden', position: 'relative' }}>
      <div style={{ position: 'absolute', top: 0, left: 0, right: 0, padding: '12px 16px', background: 'rgba(25,25,25,0.8)', backdropFilter: 'blur(10px)', zIndex: 10, borderBottom: '1px solid var(--tg-theme-hint-color, #ffffff11)', display: 'flex', alignItems: 'center', gap: '8px', fontSize: '13px', fontWeight: 600, color: 'var(--tg-theme-hint-color, #888)' }}>
        <div style={{ width: 8, height: 8, borderRadius: '50%', background: '#ef4444', boxShadow: '0 0 8px #ef4444' }} />
        LIVE MODERATION FEED
      </div>
      <div style={{ padding: '50px 12px 12px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
        <AnimatePresence>
          {events.map((ev) => (
            <motion.div
              key={ev.id}
              initial={{ opacity: 0, x: -20, scale: 0.95 }}
              animate={{ opacity: 1, x: 0, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              transition={{ type: "spring", stiffness: 400, damping: 25 }}
              className="card"
              style={{ padding: '12px', background: 'var(--tg-theme-secondary-bg-color, #1a1a1a)', display: 'flex', alignItems: 'flex-start', gap: '12px' }}
            >
              <div style={{ marginTop: '2px', background: '#000', padding: '6px', borderRadius: '50%' }}>
                {getIcon(ev.action)}
              </div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '2px' }}>
                  <span style={{ fontWeight: 600, fontSize: '14px' }}>
                    {ev.user_name}
                  </span>
                  <span style={{ fontSize: '12px', color: 'var(--tg-theme-hint-color, #888)' }}>
                    in {ev.chat_title}
                  </span>
                </div>
                <div style={{ fontSize: '13px', color: 'var(--tg-theme-hint-color, #bbb)', display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <span style={{ color: ev.action === 'ban' ? '#ef4444' : ev.action === 'warn' ? '#eab308' : 'var(--tg-theme-button-color, #3390ec)', fontWeight: 500 }}>
                    {getActionText(ev.action)}
                  </span>
                  {ev.reason && (
                    <>
                      <span>•</span>
                      <span style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{ev.reason}</span>
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
