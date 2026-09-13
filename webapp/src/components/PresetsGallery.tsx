import { useLang } from '../context/LangContext';
import { useChatSettings } from '../context/ChatSettingsContext';
import { Shield, Bitcoin, Briefcase, Coffee, Lock, Check } from 'lucide-react';
import { haptic } from '../lib/telegram';

export function PresetsGallery() {
  const { t } = useLang();
  const { draft, setSection, billing, openPresetPayment } = useChatSettings();

  if (!draft) return null;

  const isActive = (id: string) => {
    const f = draft.filters;
    const a = draft.antiflood;
    const c = draft.captcha;
    const d = draft.defcon;
    const core = draft.core;
    
    switch (id) {
      case 'basic':
        return a.enabled && a.limit === 5 && !c.enabled && !f.block_links && !d.enabled && core.ai_mode === 'off';
      case 'crypto':
        return a.enabled && a.limit === 3 && c.enabled && f.block_links && d.enabled && d.action === 'strict' && core.ai_mode === 'autoban';
      case 'corp':
        return a.enabled && a.limit === 10 && !c.enabled && !f.block_links && d.enabled && d.action === 'read_only' && core.ai_mode === 'quarantine';
      case 'chill':
        return !a.enabled && !c.enabled && !f.block_links && !d.enabled && core.ai_mode === 'off';
    }
    return false;
  };

  const presets = [
    {
      id: 'basic',
      icon: Shield,
      title: t('presets.basic'),
      desc: t('presets.basic.desc'),
      color: 'bg-emerald-500/10 text-emerald-600',
      pro: false,
      apply: () => {
        setSection('antiflood', { enabled: true, limit: 5, window: 10 });
        setSection('captcha', { enabled: false, mode: 'math', timeout_seconds: 60 });
        setSection('filters', { block_links: false, block_forwards: false, block_mentions: false, banned_words: [], blocked_media: [] });
        setSection('defcon', { enabled: false, threshold: 10, action: 'read_only', lock_seconds: 900 });
        setSection('core', { ...draft.core, ai_mode: 'off' });
      }
    },
    {
      id: 'crypto',
      icon: Bitcoin,
      title: t('presets.crypto'),
      desc: t('presets.crypto.desc'),
      color: 'bg-amber-500/10 text-amber-600',
      pro: true,
      apply: () => {
        setSection('antiflood', { enabled: true, limit: 3, window: 15 });
        setSection('captcha', { enabled: true, mode: 'math', timeout_seconds: 120 });
        setSection('filters', { block_links: true, block_forwards: true, block_mentions: true, banned_words: [], blocked_media: [] });
        setSection('defcon', { enabled: true, threshold: 5, action: 'strict', lock_seconds: 3600 });
        setSection('core', { ...draft.core, ai_mode: 'autoban', ai_threshold: 70 });
        setSection('ai', { ...draft.ai, thresholds: { spam: 60, scam: 50 } });
      }
    },
    {
      id: 'corp',
      icon: Briefcase,
      title: t('presets.corp'),
      desc: t('presets.corp.desc'),
      color: 'bg-blue-500/10 text-blue-600',
      pro: true,
      apply: () => {
        setSection('antiflood', { enabled: true, limit: 10, window: 30 });
        setSection('captcha', { enabled: false, mode: 'math', timeout_seconds: 60 });
        setSection('filters', { block_links: false, block_forwards: false, block_mentions: false, banned_words: [], blocked_media: [] });
        setSection('defcon', { enabled: true, threshold: 20, action: 'read_only', lock_seconds: 900 });
        setSection('core', { ...draft.core, ai_mode: 'quarantine', ai_threshold: 80 });
        setSection('ai', { ...draft.ai, thresholds: { toxicity: 60, nsfw: 50 } });
      }
    },
    {
      id: 'chill',
      icon: Coffee,
      title: t('presets.chill'),
      desc: t('presets.chill.desc'),
      color: 'bg-purple-500/10 text-purple-600',
      pro: false,
      apply: () => {
        setSection('antiflood', { enabled: false, limit: 5, window: 10 });
        setSection('captcha', { enabled: false, mode: 'math', timeout_seconds: 60 });
        setSection('filters', { block_links: false, block_forwards: false, block_mentions: false, banned_words: [], blocked_media: [] });
        setSection('defcon', { enabled: false, threshold: 10, action: 'read_only', lock_seconds: 900 });
        setSection('core', { ...draft.core, ai_mode: 'off' });
      }
    }
  ];

  return (
    <div className="w-full flex flex-col mt-1 mb-2 overflow-hidden">
      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mb-2">{t('presets.title')}</div>
      <div className="flex gap-3 overflow-x-auto snap-x snap-mandatory pb-4 pt-1 -mx-4 px-4 no-scrollbar">
        {presets.map((p) => {
          const locked = p.pro && !(billing?.purchased_presets || []).includes(p.id);
          const active = isActive(p.id);
          return (
            <div 
              key={p.id} 
              className={`snap-center shrink-0 w-[80%] max-w-[280px] bg-white dark:bg-[#0a0a0a] border ${active ? 'border-primary dark:border-primary ring-1 ring-primary/30' : 'border-neutral-200 dark:border-neutral-800/60'} rounded-2xl p-4 shadow-sm flex flex-col justify-between transition-colors`}
            >
              <div className="flex flex-col gap-2 mb-3">
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center mb-1 ${p.color}`}>
                  <p.icon size={22} />
                </div>
                <div className="font-bold text-neutral-900 dark:text-neutral-50 text-[15px]">{p.title}</div>
                <div className="text-[13px] text-neutral-500 leading-snug">{p.desc}</div>
              </div>
              
              <button
                className={`w-full py-2.5 rounded-xl text-[13px] font-bold flex items-center justify-center gap-1.5 transition-transform active:scale-95 ${
                  locked 
                    ? 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400' 
                    : active 
                    ? 'bg-primary/10 text-primary cursor-default'
                    : 'bg-neutral-100 dark:bg-neutral-800 text-neutral-900 dark:text-neutral-50 hover:bg-neutral-200 dark:hover:bg-neutral-700'
                }`}
                onClick={() => {
                  if (active) return;
                  if (locked) {
                    haptic('warning');
                    openPresetPayment(p.id);
                  } else {
                    haptic('success');
                    p.apply();
                    window.Telegram?.WebApp?.showAlert?.(t('presets.applied_alert', { name: p.title }));
                  }
                }}
              >
                {locked ? <><Lock size={14} /> 150 ⭐️</> : active ? <><Check size={14} /> {t('presets.active')}</> : <><Check size={14} /> {t('presets.apply')}</>}
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
}
