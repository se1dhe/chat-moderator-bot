import { useState, useEffect } from 'react';
import { Download, ShieldAlert, CheckCircle2 } from 'lucide-react';
import { useParams } from 'react-router-dom';
import { useLang } from '../context/LangContext';
import { api } from '../lib/api';
import { initData } from '../lib/telegram';
import { AuditLog } from '../lib/types';
import { Spinner } from '../components/ui';

export function Audit() {
  const { cid } = useParams<{ cid: string }>();
  const { t } = useLang();
  
  const [logs, setLogs] = useState<AuditLog[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  
  // NOTE: For true infinite scroll, we would manage page/hasMore state.
  // The current API doesn't support pagination, it just accepts limit.
  // We'll simulate the UX by requesting 100 limit, and displaying them in new mobile cards.

  useEffect(() => {
    let alive = true;
    if (!cid) return;
    
    api.audit(cid, 100)
      .then((d) => alive && setLogs(d))
      .catch((err) => {
        if (alive) {
          setError(err.message);
          setLogs([]);
        }
      });
    return () => { alive = false; };
  }, [cid]);

  if (!logs && !error) return <div className="flex-1 flex items-center justify-center py-12"><Spinner /></div>;

  if (error) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-center gap-4 py-12 text-neutral-500 animate-in fade-in">
        <ShieldAlert size={48} className="text-primary" />
        <h3 className="font-semibold text-neutral-800 dark:text-neutral-200">{error}</h3>
        <button 
          className="px-6 py-2.5 bg-neutral-200 dark:bg-neutral-800 hover:bg-neutral-300 dark:hover:bg-neutral-700 rounded-xl font-medium transition-colors mt-2" 
          onClick={() => { setError(null); setLogs(null); api.audit(cid!, 100).then(setLogs).catch(e => setError(e.message)); }}
        >
          {t('common.retry')}
        </button>
      </div>
    );
  }

  if (logs && !logs.length) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-center gap-3 py-12 text-neutral-500 animate-in fade-in">
        <div className="w-16 h-16 bg-neutral-100 dark:bg-neutral-800 rounded-full flex items-center justify-center mb-2">
          <ShieldAlert size={32} className="text-neutral-400" />
        </div>
        <h3 className="text-lg font-bold text-neutral-900 dark:text-neutral-50">{t('audit.title')}</h3>
        <p className="text-sm max-w-[250px]">{t('audit.empty')}</p>
      </div>
    );
  }

  return (
    <div className="w-full flex flex-col gap-4 animate-in fade-in slide-in-from-bottom-2 duration-300">
      <div className="flex items-center justify-between mb-1 mt-2 px-1">
        <h2 className="text-xl font-bold tracking-tight text-neutral-900 dark:text-white">
          {t('audit.title')}
        </h2>
        <a 
          href={`/api/chats/${cid}/audit/export?initData=${encodeURIComponent(initData)}`} 
          className="flex items-center gap-2 px-3 py-1.5 bg-neutral-200 dark:bg-neutral-800 rounded-lg text-sm font-semibold hover:bg-neutral-300 dark:hover:bg-neutral-700 transition-colors text-neutral-700 dark:text-neutral-300"
        >
          <Download size={16} />
          <span>{t('audit.export')}</span>
        </a>
      </div>

      <div className="flex flex-col gap-3 w-full pb-4">
        {logs!.map((log) => (
          <div key={log.id} className="p-4 bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60/60/60/60 rounded-2xl shadow-sm flex items-start gap-3 w-full">
            <div className="mt-0.5 shrink-0">
              {log.action.includes('un') ? (
                <CheckCircle2 size={20} className="text-emerald-500" />
              ) : (
                <ShieldAlert size={20} className="text-primary" />
              )}
            </div>
            
            <div className="flex flex-col min-w-0 flex-1">
              <div className="flex justify-between items-center gap-2 mb-1">
                <span className="font-bold text-sm capitalize truncate text-neutral-900 dark:text-neutral-100">
                  {log.action.replace(/_/g, ' ')}
                </span>
                <span className="text-[11px] font-medium text-neutral-500 dark:text-neutral-400 shrink-0">
                  {new Date(log.created_at).toLocaleString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
              
              {log.reason && (
                <p className="text-[13px] text-neutral-600 dark:text-neutral-400 line-clamp-2 break-words leading-snug">
                  {log.reason}
                </p>
              )}
              
              {log.user_id && (
                <div className="mt-2.5 text-[10px] font-mono bg-neutral-100 dark:bg-neutral-800 px-2 py-1 rounded-md inline-flex self-start text-neutral-500">
                  UID: {log.user_id}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
