import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { BarChart3, Lock, Sparkles, ServerCrash } from 'lucide-react';
import { useLang } from '../context/LangContext';
import { useChatSettings } from '../context/ChatSettingsContext';
import { api } from '../lib/api';
import { Spinner } from '../components/ui';

interface TimelineDay {
  key: string;
  day: number;
  count: number;
}

function last14(timeline: Record<string, number>): TimelineDay[] {
  const out = [];
  const now = new Date();
  for (let i = 13; i >= 0; i--) {
    const d = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate() - i));
    const key = d.toISOString().slice(0, 10);
    out.push({ key, day: d.getUTCDate(), count: timeline[key] || 0 });
  }
  return out;
}

export function Stats() {
  const { cid } = useParams<{ cid: string }>();
  const { t } = useLang();
  const { pro, billing, openUpgrade } = useChatSettings();
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!pro) return; 
    let alive = true;
    if (!cid) return;
    api.stats(cid)
      .then((d) => alive && setData(d))
      .catch((err) => {
        if (alive) {
          setError(err.message);
          setData({ actions: {}, pending_quarantine: 0, timeline: {}, categories: {}, members: 0 });
        }
      });
    return () => { alive = false; };
  }, [cid, pro]);

  if (billing === null) return <div className="flex-1 flex items-center justify-center py-12"><Spinner /></div>;
  if (!pro) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-center gap-4 py-12 text-neutral-500 animate-in fade-in slide-in-from-bottom-2">
        <div className="w-20 h-20 bg-amber-100 dark:bg-amber-900/30 rounded-full flex items-center justify-center text-amber-500 mb-2">
          <Lock size={40} />
        </div>
        <h3 className="text-xl font-bold text-neutral-900 dark:text-neutral-50">{t('stats.proTitle')}</h3>
        <p className="text-sm max-w-[250px] mb-2">{t('stats.proPitch')}</p>
        <button 
          className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-400 hover:to-orange-400 text-white rounded-xl font-bold transition-transform active:scale-95 shadow-lg shadow-amber-500/20" 
          onClick={openUpgrade}
        >
          <Sparkles size={18} /> {t('pro.upgrade')}
        </button>
      </div>
    );
  }

  if (!data && !error) return <div className="flex-1 flex items-center justify-center py-12"><Spinner /></div>;

  if (error) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-center gap-4 py-12 text-neutral-500 animate-in fade-in">
        <ServerCrash size={48} className="text-primary" />
        <h3 className="font-semibold text-neutral-800 dark:text-neutral-200">{error}</h3>
        <button 
          className="px-6 py-2.5 bg-neutral-200 dark:bg-neutral-800 hover:bg-neutral-300 dark:hover:bg-neutral-700 rounded-xl font-medium transition-colors mt-2" 
          onClick={() => { setError(null); setData(null); api.stats(cid!).then(setData).catch(e => setError(e.message)); }}
        >
          {t('common.retry')}
        </button>
      </div>
    );
  }

  const actions = Object.entries(data.actions as Record<string, number>).sort((a, b) => b[1] - a[1]);
  const total = actions.reduce((n, [, v]) => n + v, 0);
  const maxAction = actions.length ? actions[0][1] : 1;

  const days = last14(data.timeline || {});
  const maxDay = Math.max(1, ...days.map((d) => d.count));

  const cats = Object.entries(data.categories as Record<string, number> || {}).filter(([c]) => c !== 'ok').sort((a, b) => b[1] - a[1]);
  const maxCat = cats.length ? cats[0][1] : 1;

  return (
    <div className="w-full flex flex-col gap-5 animate-in fade-in slide-in-from-bottom-2 duration-300 mt-2">
      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1">{t('stats.title')}</div>
      <div className="grid grid-cols-2 gap-3 w-full">
        <div className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-2xl p-4 flex flex-col justify-center shadow-sm">
          <div className="text-2xl font-black text-neutral-900 dark:text-neutral-50">{total}</div>
          <div className="text-xs font-semibold text-neutral-500 uppercase tracking-wide mt-1">{t('stats.total')}</div>
        </div>
        <div className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-2xl p-4 flex flex-col justify-center shadow-sm">
          <div className={`text-2xl font-black ${data.pending_quarantine ? 'text-amber-500' : 'text-neutral-900 dark:text-neutral-50'}`}>{data.pending_quarantine}</div>
          <div className="text-xs font-semibold text-neutral-500 uppercase tracking-wide mt-1">{t('stats.pending')}</div>
        </div>
        <div className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-2xl p-4 flex flex-col justify-center shadow-sm">
          <div className="text-2xl font-black text-neutral-900 dark:text-neutral-50">{data.members || 0}</div>
          <div className="text-xs font-semibold text-neutral-500 uppercase tracking-wide mt-1">{t('stats.members')}</div>
        </div>
        <div className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-2xl p-4 flex flex-col justify-center shadow-sm">
          <div className="text-2xl font-black text-neutral-900 dark:text-neutral-50">{cats.reduce((n, [, v]) => n + v, 0)}</div>
          <div className="text-xs font-semibold text-neutral-500 uppercase tracking-wide mt-1">{t('stats.categories')}</div>
        </div>
      </div>

      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-2">{t('stats.last14')}</div>
      <div className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-2xl p-4 shadow-sm w-full">
        <div className="flex items-end gap-1 h-28">
          {days.map((d) => (
            <div className="flex-1 flex flex-col items-center gap-1 h-full justify-end group" key={d.key} title={`${d.key}: ${d.count}`}>
              <div 
                className="w-full min-h-[4px] bg-gradient-to-t from-primary/80 to-primary-light rounded-t-sm transition-all group-hover:opacity-80" 
                style={{ height: `${(d.count / maxDay) * 100}%` }} 
              />
              <div className="text-[10px] text-neutral-400 font-mono">{d.day}</div>
            </div>
          ))}
        </div>
      </div>

      {cats.length > 0 && (
        <>
          <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-2">{t('stats.categories')}</div>
          <div className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-2xl p-4 shadow-sm w-full flex flex-col gap-3">
            {cats.map(([cat, n]) => (
              <div key={cat} className="flex items-center gap-3 w-full">
                <span className="w-20 text-xs font-medium text-neutral-600 dark:text-neutral-400 capitalize truncate">
                  {t(`cat.${cat}`) !== `cat.${cat}` ? t(`cat.${cat}`) : cat}
                </span>
                <div className="flex-1 h-2.5 bg-neutral-100 dark:bg-neutral-800 rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-primary to-primary-light rounded-full" style={{ width: `${(n / maxCat) * 100}%` }} />
                </div>
                <span className="w-8 text-right text-xs font-bold text-neutral-900 dark:text-neutral-50 font-mono">{n}</span>
              </div>
            ))}
          </div>
        </>
      )}

      {actions.length > 0 ? (
        <>
          <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-2">{t('stats.actions')}</div>
          <div className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-2xl p-4 shadow-sm w-full flex flex-col gap-3">
            {actions.map(([action, n]) => (
              <div key={action} className="flex items-center gap-3 w-full">
                <span className="w-20 text-xs font-medium text-neutral-600 dark:text-neutral-400 capitalize truncate">
                  {action.replace(/_/g, ' ')}
                </span>
                <div className="flex-1 h-2.5 bg-neutral-100 dark:bg-neutral-800 rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-primary to-primary-light rounded-full" style={{ width: `${(n / maxAction) * 100}%` }} />
                </div>
                <span className="w-8 text-right text-xs font-bold text-neutral-900 dark:text-neutral-50 font-mono">{n}</span>
              </div>
            ))}
          </div>
        </>
      ) : (
        <div className="flex-1 flex flex-col items-center justify-center text-center gap-3 py-12 text-neutral-500">
          <BarChart3 size={44} className="text-neutral-300 dark:text-neutral-700" />
          <p className="text-sm">{t('stats.empty')}</p>
        </div>
      )}
    </div>
  );
}
