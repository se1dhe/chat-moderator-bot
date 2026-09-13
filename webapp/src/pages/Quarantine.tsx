import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { ShieldCheck, Check, Ban, Ruler, ShieldAlert } from 'lucide-react';
import { useLang } from '../context/LangContext';
import { api } from '../lib/api';
import { Spinner } from '../components/ui';
import { haptic } from '../lib/telegram';

export function Quarantine() {
  const { cid } = useParams<{ cid: string }>();
  const { t } = useLang();
  const [items, setItems] = useState<any[] | null>(null);
  const [busy, setBusy] = useState<number | null>(null);

  useEffect(() => {
    let alive = true;
    if (!cid) return;
    api.quarantine(cid).then((d) => alive && setItems(d)).catch(() => alive && setItems([]));
    return () => { alive = false; };
  }, [cid]);

  const decide = async (vid: number, action: string) => {
    setBusy(vid);
    try {
      await api.decide(cid!, vid, action);
      haptic(action === 'approve' ? 'success' : 'warning');
      setItems((list) => list!.filter((v) => v.id !== vid));
    } catch (e: any) {
      haptic('error');
      window.Telegram?.WebApp?.showAlert?.(e.message || 'Error processing decision');
    } finally {
      setBusy(null);
    }
  };

  if (!items) return <div className="flex-1 flex items-center justify-center py-12"><Spinner /></div>;

  if (!items.length) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-center gap-3 py-12 text-neutral-500 animate-in fade-in">
        <div className="w-16 h-16 bg-emerald-500/10 rounded-full flex items-center justify-center mb-2">
          <ShieldCheck size={32} className="text-emerald-500" />
        </div>
        <h3 className="text-lg font-bold text-neutral-900 dark:text-neutral-50">{t('nav.quarantine')}</h3>
        <p className="text-sm max-w-[250px]">{t('quar.empty')}</p>
      </div>
    );
  }

  return (
    <div className="w-full flex flex-col gap-4 animate-in fade-in slide-in-from-bottom-2 duration-300">
      <div className="flex items-center justify-between mb-1 mt-2 px-1">
        <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider">{t('quar.title')} <span className="ml-1 px-1.5 py-0.5 bg-neutral-200 dark:bg-neutral-800 rounded-md text-neutral-900 dark:text-neutral-50 font-bold">{items.length}</span></div>
      </div>

      <div className="flex flex-col gap-3 w-full pb-4">
        {items.map((v) => (
          <div key={v.id} className="p-4 bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-2xl shadow-sm flex flex-col gap-3 w-full relative overflow-hidden">
            {v.score > 80 && (
              <div className="absolute top-0 right-0 w-16 h-16 bg-primary/5 rounded-bl-full pointer-events-none" />
            )}
            
            <div className="flex items-center justify-between">
              <span className="text-[13px] font-bold uppercase tracking-wider text-neutral-900 dark:text-white flex items-center gap-1.5">
                <ShieldAlert size={14} className="text-amber-500" />
                {t(`cat.${v.category}`) || v.category}
              </span>
              <span className="px-2 py-0.5 bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400 border border-amber-500/20 text-[11px] font-bold rounded-md">
                {v.score}% {t('quar.confidence')}
              </span>
            </div>
            
            <div className="text-[11px] font-medium text-neutral-500 flex items-center gap-1">
              {t('quar.from')}: <code className="bg-neutral-100 dark:bg-neutral-800 px-1.5 py-0.5 rounded text-neutral-400">{v.user_id}</code>
            </div>
            
            {v.text && (
              <div className="p-3 bg-neutral-50 dark:bg-neutral-950 border border-neutral-200 dark:border-neutral-800 rounded-xl text-[13px] text-neutral-700 dark:text-neutral-300 break-words leading-relaxed">
                {v.text}
              </div>
            )}
            
            {v.explanation && (
              <div className="text-[12px] font-medium text-amber-600 dark:text-amber-400 leading-snug">
                {v.explanation}
              </div>
            )}
            
            <div className="flex flex-wrap gap-2 w-full mt-2">
              <button 
                className={`flex-1 min-w-[80px] flex items-center justify-center gap-1.5 px-3 py-2.5 bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400 hover:bg-emerald-200 dark:hover:bg-emerald-900/50 rounded-xl text-[13px] font-bold transition-transform active:scale-95 ${busy === v.id ? 'opacity-50 pointer-events-none' : ''}`} 
                disabled={busy === v.id} 
                onClick={() => decide(v.id, 'approve')}
              >
                <Check size={16} /> {t('quar.approve')}
              </button>
              <button 
                className={`flex-1 min-w-[80px] flex items-center justify-center gap-1.5 px-3 py-2.5 bg-red-500 hover:bg-red-600 text-white rounded-xl text-[13px] font-bold shadow-md shadow-red-500/20 transition-transform active:scale-95 ${busy === v.id ? 'opacity-50 pointer-events-none' : ''}`} 
                disabled={busy === v.id} 
                onClick={() => decide(v.id, 'ban')}
              >
                <Ban size={16} /> {t('quar.ban')}
              </button>
              <button 
                className={`w-[60px] shrink-0 flex items-center justify-center gap-1.5 px-0 py-2.5 bg-neutral-100 dark:bg-neutral-800 text-neutral-600 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-700 rounded-xl transition-transform active:scale-95 ${busy === v.id ? 'opacity-50 pointer-events-none' : ''}`} 
                disabled={busy === v.id} 
                onClick={() => decide(v.id, 'rule')}
                title={t('quar.rule')}
              >
                <Ruler size={16} />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
