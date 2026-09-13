import { useState } from 'react';
import { Crown, Sparkles } from 'lucide-react';
import { useLang } from '../context/LangContext';
import { useChatSettings } from '../context/ChatSettingsContext';

const fmtDate = (iso?: string) => (iso ? new Date(iso).toLocaleDateString() : '');

export function ProBanner() {
  const { t } = useLang();
  const { billing, pro, openUpgrade } = useChatSettings();
  const [busy, setBusy] = useState(false);

  if (!billing) return null;

  if (pro) {
    return (
      <div className="w-full flex items-center gap-3 p-4 rounded-2xl border border-amber-500/30 bg-gradient-to-r from-amber-500/10 to-transparent">
        <Crown size={24} className="text-amber-500 shrink-0" />
        <div className="flex-1 min-w-0">
          <div className="font-bold text-amber-500 text-sm">{t('pro.active')}</div>
          <div className="text-[11px] text-amber-600/70 dark:text-amber-400/70 mt-0.5">{t('pro.until', { date: fmtDate(billing.active_until) })}</div>
        </div>
        <span className="shrink-0 px-2 py-0.5 bg-amber-500/20 text-amber-600 dark:text-amber-400 text-[10px] font-bold uppercase rounded-md border border-amber-500/30">{t('pro.badge')}</span>
      </div>
    );
  }

  const upgrade = async () => {
    setBusy(true);
    try { await openUpgrade(); } finally { setBusy(false); }
  };

  return (
    <button 
      className="w-full flex items-center gap-3 p-4 rounded-2xl border border-primary/30 bg-gradient-to-r from-primary/10 to-primary/5 hover:from-primary/15 transition-all text-left active:scale-[0.98]" 
      onClick={upgrade} 
      disabled={busy}
    >
      <Sparkles size={24} className="text-primary shrink-0 drop-shadow-[0_0_8px_rgba(220,38,38,0.5)] drop-shadow-[0_0_8px_rgba(220,38,38,0.5)] drop-shadow-[0_0_8px_rgba(220,38,38,0.5)] drop-shadow-[0_0_8px_rgba(220,38,38,0.5)]" />
      <div className="flex-1 min-w-0">
        <div className="font-bold text-neutral-900 dark:text-neutral-50 text-sm">{busy ? t('pro.opening') : t('pro.upgrade')}</div>
        <div className="text-[11px] text-neutral-500 mt-0.5 leading-tight">{t('pro.pitch')}</div>
      </div>
      <span className="shrink-0 text-sm font-black text-amber-500">{t('pro.price', { stars: billing.price_stars, days: billing.period_days })}</span>
    </button>
  );
}
