import { useNavigate, useParams } from 'react-router-dom';
import {
  ShieldCheck, Gauge, Filter, Moon, BrainCircuit, Siren, AlertTriangle, UserCheck,
  ChevronRight, ServerCrash, Lock, Shield,
} from 'lucide-react';
import { motion } from 'framer-motion';
import { useLang } from '../context/LangContext';
import { useChatSettings } from '../context/ChatSettingsContext';
import { Spinner, Segmented, Row, Toggle } from '../components/ui';
import { ProBanner } from '../components/ProBanner';
import { Tips } from '../components/Tips';
import { OnboardingWizard } from '../components/OnboardingWizard';
import { haptic } from '../lib/telegram';

const LANGS = [{ value: 'en', label: 'EN' }, { value: 'ru', label: 'RU' }, { value: 'uk', label: 'UK' }];

export function Dashboard() {
  const { t } = useLang();
  const { cid } = useParams<{ cid: string }>();
  const navigate = useNavigate();
  const { draft, error, reload, setSection, pro, openUpgrade } = useChatSettings();

  if (error) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-center gap-4 py-12 text-neutral-500">
        <ServerCrash size={48} className="text-primary" />
        <h3 className="font-semibold text-neutral-800 dark:text-neutral-200">{t('common.error')}</h3>
        <button 
          className="px-6 py-2.5 bg-neutral-200 dark:bg-neutral-800 hover:bg-neutral-300 dark:hover:bg-neutral-700 rounded-xl font-medium transition-colors mt-2" 
          onClick={reload}
        >
          {t('common.retry')}
        </button>
      </div>
    );
  }
  if (!draft) return <div className="flex-1 flex items-center justify-center py-12"><Spinner /></div>;

  if (draft.onboarding?.setup_completed === false) {
    return <OnboardingWizard />;
  }

  const f = draft.filters;
  const filtersOn = f.block_links || f.block_forwards || f.block_mentions
    || f.banned_words.length > 0 || f.blocked_media.length > 0;
  const modesOn = draft.modes.night.enabled || draft.modes.silent || draft.modes.slow_seconds > 0;

  const groups = [
    {
      label: t('dash.protection'),
      items: [
        { key: 'rbac', icon: Shield, title: t('sec.rbac'), desc: t('sec.rbac.desc'), on: true },
        { key: 'captcha', icon: ShieldCheck, title: t('sec.captcha'), desc: t('sec.captcha.desc'), on: draft.captcha.enabled },
        { key: 'raid', icon: Siren, title: t('sec.raid'), desc: t('sec.raid.desc'), on: draft.raid.enabled, pro: true },
        { key: 'warns', icon: AlertTriangle, title: t('sec.warns'), desc: t('sec.warns.desc'), on: true, state: `${draft.core.warn_limit} → ${t(`action.${draft.core.warn_action}`)}` },
      ],
    },
    {
      label: t('dash.content'),
      items: [
        { key: 'welcome', icon: UserCheck, title: t('sec.welcome'), desc: t('sec.welcome.desc'), on: !!draft.onboarding?.welcome_message },
        { key: "triggers", icon: ShieldCheck, title: t('sec.triggers'), desc: t('sec.triggers.desc'), on: true },
        { key: "autocomment", icon: Filter, title: t('sec.autocomment'), desc: t('sec.autocomment.desc'), on: draft.auto_comment?.enabled, pro: true },
        { key: 'antiflood', icon: Gauge, title: t('sec.antiflood'), desc: t('sec.antiflood.desc'), on: draft.antiflood.enabled },
        { key: 'filters', icon: Filter, title: t('sec.filters'), desc: t('sec.filters.desc'), on: filtersOn },
        { key: 'modes', icon: Moon, title: t('sec.modes'), desc: t('sec.modes.desc'), on: modesOn },
      ],
    },
    {
      label: t('dash.intelligence'),
      items: [
        { key: 'ai', icon: BrainCircuit, title: t('sec.ai'), desc: t('sec.ai.desc'), on: draft.core.ai_mode !== 'off', state: draft.core.ai_mode !== 'off' ? t(`ai.mode.${draft.core.ai_mode}`) : undefined },
        { key: 'exempt', icon: UserCheck, title: t('sec.exempt'), desc: t('sec.exempt.desc'), on: draft.exempt_user_ids.length > 0, state: draft.exempt_user_ids.length ? String(draft.exempt_user_ids.length) : undefined },
      ],
    },
  ];


  return (
    <div className="w-full flex flex-col gap-4 animate-in fade-in slide-in-from-bottom-2 duration-300">
      <ProBanner />

      <Tips chatId={cid} />

      <div>
        <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider mb-2 ml-1">{t('dash.chatLang')}</div>
        <Segmented value={draft.lang} onChange={(v: string) => setSection('lang', v)} options={LANGS} />
      </div>

      <div>
        <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider mb-2 ml-1">{t('dash.privacy')}</div>
        <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60 rounded-2xl p-4 shadow-sm">
          <Row title={t('dash.privacy')} desc={t('dash.privacy.desc')}>
            <Toggle 
              checked={draft.core.anonymize_events ?? false}
              onChange={(v: boolean) => setSection('core', { ...draft.core, anonymize_events: v })}
            />
          </Row>
        </div>
      </div>

      {groups.map((g) => (
        <motion.div key={g.label}  className="w-full flex flex-col gap-2">
          <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider mt-2 ml-1">{g.label}</div>
          <div className="flex flex-col gap-2">
            {g.items.map((it) => {
              const locked = it.pro && !pro;
              return (
                <motion.button
                  whileTap={{ scale: 0.97 }}
                  key={it.key}
                  className="w-full flex items-center p-4 bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60 rounded-2xl shadow-sm hover:border-primary/30 dark:hover:border-primary/30 active:bg-neutral-50 dark:active:bg-neutral-800 transition-all text-left group"
                  onClick={() => {
                    haptic('light');
                    if (locked) openUpgrade();
                    else navigate(`/c/${cid}/s/${it.key}`);
                  }}
                >
                  <div className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 mr-4 transition-colors ${
                    !locked && it.on ? 'bg-primary/10 text-primary dark:bg-primary/20 dark:text-primary-light' : 'bg-neutral-100 dark:bg-neutral-800 text-neutral-500'
                  }`}>
                    <it.icon size={20} />
                  </div>
                  
                  <div className="flex-1 min-w-0 pr-2">
                    <div className="font-bold text-neutral-900 dark:text-neutral-50 truncate leading-tight mb-0.5">
                      {it.title}
                    </div>
                    <div className="text-[13px] text-neutral-500 truncate">
                      {it.desc}
                    </div>
                  </div>

                  {locked ? (
                    <span className="shrink-0 flex items-center gap-1 px-2 py-1 bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400 text-[10px] font-bold uppercase rounded-md">
                      <Lock size={10} /> PRO
                    </span>
                  ) : (
                    <span className={`shrink-0 text-xs font-semibold ${it.on ? 'text-primary' : 'text-neutral-400'}`}>
                      {it.state ?? (it.on ? t('dash.enabled') : t('dash.disabled'))}
                    </span>
                  )}
                  
                  <ChevronRight size={18} className="text-neutral-300 dark:text-neutral-600 shrink-0 ml-2 group-hover:text-neutral-500 transition-colors" />
                </motion.button>
              );
            })}
          </div>
        </motion.div>
      ))}
    </div>
  );
}
