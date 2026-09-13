import { useEffect, useState, useCallback, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { Users, Search, TriangleAlert, VolumeX, Volume2, UserMinus, Ban, RotateCcw } from 'lucide-react';
import { useLang } from '../context/LangContext';
import { api } from '../lib/api';
import { Spinner } from '../components/ui';
import { haptic, showConfirm, showAlert } from '../lib/telegram';

const META: Record<string, any> = {
  warn: { icon: TriangleAlert, cls: 'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400 hover:bg-amber-200 dark:hover:bg-amber-900/50' },
  mute: { icon: VolumeX, cls: 'bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-400 hover:bg-orange-200 dark:hover:bg-orange-900/50', duration: true },
  unmute: { icon: Volume2, cls: 'bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-700' },
  kick: { icon: UserMinus, cls: 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 hover:bg-red-200 dark:hover:bg-red-900/50', confirm: true },
  ban: { icon: Ban, cls: 'bg-red-500 hover:bg-red-600 text-white shadow-md shadow-red-500/20', confirm: true, duration: true },
  unban: { icon: RotateCcw, cls: 'bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-700' },
};

const actionsFor = (state: string) => {
  if (state === 'banned') return ['unban'];
  if (state === 'muted') return ['warn', 'unmute', 'kick', 'ban'];
  return ['warn', 'mute', 'kick', 'ban'];
};

const DURATIONS = [
  { key: '1h', minutes: 60 },
  { key: '8h', minutes: 480 },
  { key: '1d', minutes: 1440 },
  { key: '7d', minutes: 10080 },
  { key: 'perm', minutes: 0 },
];

const nameOf = (m: any) => m.full_name || (m.username ? `@${m.username}` : `#${m.user_id}`);

export function Members() {
  const { cid } = useParams<{ cid: string }>();
  const { t } = useLang();
  const [q, setQ] = useState('');
  const [rows, setRows] = useState<any[] | null>(null);
  const [busy, setBusy] = useState<string | null>(null);
  const [reasons, setReasons] = useState<Record<string, string>>({});
  const [durs, setDurs] = useState<Record<string, number>>({});
  
  const abortCtrlRef = useRef<AbortController | null>(null);

  const load = useCallback((query: string) => {
    if (abortCtrlRef.current) abortCtrlRef.current.abort();
    const ctrl = new AbortController();
    abortCtrlRef.current = ctrl;
    
    if (!cid) return;
    
    api.members(cid, query, { signal: ctrl.signal })
      .then(setRows)
      .catch((e) => {
        if (e.name !== 'AbortError') setRows([]);
      });
  }, [cid]);

  useEffect(() => {
    const id = setTimeout(() => load(q), 250);
    return () => clearTimeout(id);
  }, [q, load]);

  const act = async (m: any, key: string) => {
    const meta = META[key];
    if (meta.confirm) {
      const ok = await showConfirm(t('members.confirm', { action: t(`act.${key}`), name: nameOf(m) }));
      if (!ok) return;
    }
    setBusy(`${m.user_id}:${key}`);
    haptic(meta.cls.includes('bg-red') ? 'warning' : 'light');
    try {
      const reason = (reasons[m.user_id] || '').trim();
      const extra = meta.duration ? { minutes: durs[m.user_id] ?? 60 } : {};
      await api.memberAction(cid!, m.user_id, key, { ...extra, reason });
      haptic('success');
      load(q);
    } catch (err: any) {
      haptic('error');
      showAlert(t('common.error') + ': ' + err.message);
    } finally {
      setBusy(null);
    }
  };

  return (
    <div className="w-full flex flex-col animate-in fade-in slide-in-from-bottom-2 duration-300">
      <div className="sticky top-14 z-30 px-4 py-3 bg-neutral-50/90 dark:bg-neutral-950/90 backdrop-blur-md">
        <div className="relative w-full">
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
            <Search size={18} className="text-neutral-400" />
          </div>
          <input 
            className="w-full pl-10 pr-4 py-3 bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-xl focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/50 transition-all font-medium text-[15px]" 
            value={q} 
            placeholder={t('members.search')}
            onChange={(e) => setQ(e.target.value)} 
          />
        </div>
      </div>

      <div className="px-4 pb-4 flex flex-col gap-3">
        {rows === null ? (
          <div className="flex-1 flex items-center justify-center py-12"><Spinner /></div>
        ) : rows.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center text-center gap-3 py-12 text-neutral-500">
            <Users size={44} className="text-neutral-300 dark:text-neutral-700" />
            <p className="text-sm font-medium">{t('members.empty')}</p>
          </div>
        ) : (
          rows.map((m) => {
            const acts = actionsFor(m.state);
            const showDuration = acts.some((k) => META[k].duration);
            const sel = durs[m.user_id] ?? 60;
            return (
              <div key={m.user_id} className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-2xl shadow-sm p-4 w-full flex flex-col gap-3">
                <div className="flex items-start justify-between min-w-0">
                  <div className="flex flex-col min-w-0 pr-2">
                    <div className="flex items-center gap-2 mb-0.5 flex-wrap">
                      <span className="font-bold text-base text-neutral-900 dark:text-neutral-50 truncate leading-tight">
                        {nameOf(m)}
                      </span>
                      {m.state === 'banned' && <span className="px-1.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400">{t('members.banned')}</span>}
                      {m.state === 'muted' && <span className="px-1.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-orange-100 text-orange-600 dark:bg-orange-900/30 dark:text-orange-400">{t('members.muted')}</span>}
                    </div>
                    <div className="text-[13px] text-neutral-500 flex items-center gap-1.5 flex-wrap">
                      {m.username && <span>@{m.username}</span>}
                      {m.username && <span className="text-neutral-300 dark:text-neutral-700">•</span>}
                      <code className="text-[11px] bg-neutral-100 dark:bg-neutral-800 px-1 py-0.5 rounded text-neutral-400">{m.user_id}</code>
                      <span className="text-neutral-300 dark:text-neutral-700">•</span>
                      <span>{t('members.messages', { count: m.message_count })}</span>
                    </div>
                  </div>
                </div>

                <input
                  className="w-full px-3 py-2 bg-neutral-50 dark:bg-neutral-950 border border-neutral-200 dark:border-neutral-800 rounded-lg text-[13px] focus:outline-none focus:border-primary/50 transition-colors"
                  value={reasons[m.user_id] || ''}
                  placeholder={t('members.reason')}
                  onChange={(e) => setReasons((r) => ({ ...r, [m.user_id]: e.target.value }))}
                />
                
                {showDuration && (
                  <div className="flex items-center justify-between w-full">
                    <span className="text-xs font-semibold text-neutral-500 uppercase tracking-wider">{t('members.duration')}</span>
                    <div className="flex gap-1">
                      {DURATIONS.map((d) => (
                        <button key={d.key}
                          className={`px-2 py-1 text-[11px] font-bold rounded-md transition-colors ${sel === d.minutes ? 'bg-neutral-800 text-white dark:bg-neutral-100 dark:text-neutral-900 shadow-sm' : 'bg-neutral-100 dark:bg-neutral-800 text-neutral-500 hover:text-neutral-900 dark:hover:text-white'}`}
                          onClick={() => { haptic('light'); setDurs((r) => ({ ...r, [m.user_id]: d.minutes })); }}>
                          {t(`dur.${d.key}`)}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
                
                <div className="flex flex-wrap gap-2 w-full mt-1">
                  {acts.map((key) => {
                    const meta = META[key];
                    const Icon = meta.icon;
                    return (
                      <button key={key} 
                        className={`flex-1 min-w-[70px] flex items-center justify-center gap-1.5 px-2.5 py-2 rounded-xl text-[13px] font-bold transition-transform active:scale-95 ${meta.cls} ${busy === `${m.user_id}:${key}` ? 'opacity-50 pointer-events-none' : ''}`}
                        disabled={busy === `${m.user_id}:${key}`}
                        onClick={() => act(m, key)}>
                        <Icon size={16} className={meta.cls.includes('bg-red-500') ? 'text-white' : ''} /> 
                        {t(`act.${key}`)}
                      </button>
                    );
                  })}
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
