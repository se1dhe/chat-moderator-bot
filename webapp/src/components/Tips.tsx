import { useEffect, useState } from 'react';
import { Lightbulb, ShieldCheck } from 'lucide-react';
import { useLang } from '../context/LangContext';
import { useChatSettings } from '../context/ChatSettingsContext';
import { api } from '../lib/api';

function buildTips(d: any, stats: any) {
  const tips = [];
  const f = d.filters;
  if (!d.captcha.enabled) tips.push('tips.captcha');
  if (!d.antiflood.enabled) tips.push('tips.antiflood');
  if (d.core.ai_mode === 'off') tips.push('tips.ai');
  else tips.push(null);
  if (!d.raid.enabled) tips.push('tips.raid');
  if (!f.block_links && f.banned_words.length === 0 && f.blocked_media.length === 0) tips.push('tips.filters');
  if (stats && stats.pending_quarantine > 0) tips.push('tips.quarantine');
  return tips.filter(Boolean);
}

export function Tips({ chatId }: { chatId: string | number }) {
  const { t } = useLang();
  const { draft } = useChatSettings();
  const [stats, setStats] = useState<any>(null);

  useEffect(() => { api.stats(chatId).then(setStats).catch(() => setStats(null)); }, [chatId]);

  if (!draft) return null;
  const tips = buildTips(draft, stats).slice(0, 3) as string[];

  return (
    <div className="w-full flex flex-col gap-2">
      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1">{t('tips.title')}</div>
      {tips.length === 0 ? (
        <div className="flex items-center gap-3 p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-700 dark:text-emerald-400">
          <ShieldCheck size={20} className="shrink-0" />
          <span className="text-[13px] font-medium">{t('tips.allGood')}</span>
        </div>
      ) : (
        tips.map((k) => (
          <div className="flex items-center gap-3 p-3 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-700 dark:text-amber-400" key={k}>
            <Lightbulb size={20} className="shrink-0" />
            <span className="text-[13px] font-medium leading-tight">{t(k)}</span>
          </div>
        ))
      )}
    </div>
  );
}
