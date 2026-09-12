import { useNavigate, useParams } from 'react-router-dom'
import {
  ShieldCheck, Gauge, Filter, Moon, BrainCircuit, Siren, AlertTriangle, UserCheck,
  ChevronRight, ServerCrash, Lock,
} from 'lucide-react'
import { motion } from 'framer-motion'
import { useLang } from '../context/LangContext'
import { useChatSettings } from '../context/ChatSettingsContext'
import { Spinner, Segmented, SwitchRow } from '../components/ui'
import { ProBanner } from '../components/ProBanner'
import { Tips } from '../components/Tips'
import { OnboardingWizard } from '../components/OnboardingWizard'
import { haptic } from '../lib/telegram'

const LANGS = [{ value: 'en', label: 'EN' }, { value: 'ru', label: 'RU' }, { value: 'uk', label: 'UK' }]

export function Dashboard() {
  const { t } = useLang()
  const { cid } = useParams()
  const navigate = useNavigate()
  const { draft, error, reload, setSection, pro, openUpgrade } = useChatSettings()

  if (error) {
    return (
      <div className="content">
        <div className="center-state">
          <ServerCrash size={44} className="ico" />
          <h3>{t('common.error')}</h3>
          <button className="btn" onClick={reload}>{t('common.retry')}</button>
        </div>
      </div>
    )
  }
  if (!draft) return <div className="content"><Spinner /></div>

  if (draft.onboarding?.setup_completed === false) {
    return <OnboardingWizard />
  }

  const f = draft.filters
  const filtersOn = f.block_links || f.block_forwards || f.block_mentions
    || f.banned_words.length > 0 || f.blocked_media.length > 0
  const modesOn = draft.modes.night.enabled || draft.modes.silent || draft.modes.slow_seconds > 0

  const groups = [
    {
      label: t('dash.protection'),
      items: [
        { key: 'captcha', icon: ShieldCheck, title: t('sec.captcha'), desc: t('sec.captcha.desc'), on: draft.captcha.enabled },
        { key: 'raid', icon: Siren, title: t('sec.raid'), desc: t('sec.raid.desc'), on: draft.raid.enabled, pro: true },
        { key: 'warns', icon: AlertTriangle, title: t('sec.warns'), desc: t('sec.warns.desc'), on: true, state: `${draft.core.warn_limit} → ${t(`action.${draft.core.warn_action}`)}` },
      ],
    },
    {
      label: t('dash.content'),
      items: [
        { key: 'autocomment', icon: Filter, title: 'Auto-Comment', desc: 'First comment in discussions', on: draft.auto_comment?.enabled, pro: true },
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
  ]

  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.05
      }
    }
  }

  const item = {
    hidden: { opacity: 0, y: 15, scale: 0.95 },
    show: { opacity: 1, y: 0, scale: 1, transition: { type: "spring", stiffness: 300, damping: 24 } }
  }

  return (
    <div className="content fade-in">
      <ProBanner />

      <Tips chatId={cid} />

      <div className="section-label">{t('dash.chatLang')}</div>
      <Segmented value={draft.lang} onChange={(v) => setSection('lang', v)} options={LANGS} />

      <div className="section-label">Privacy</div>
      <div className="card">
        <SwitchRow 
          label={t('dash.privacy')}
          desc={t('dash.privacy.desc')}
          checked={draft.core.anonymize_events ?? false}
          onChange={(v) => setSection('core', { ...draft.core, anonymize_events: v })}
        />
      </div>

      {groups.map((g, gi) => (
        <motion.div key={g.label} variants={container} initial="hidden" animate="show">
          <div className="section-label">{g.label}</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.55rem' }}>
            {g.items.map((it) => {
              const locked = it.pro && !pro
              return (
                <motion.button
                  variants={item}
                  whileTap={{ scale: 0.97 }}
                  key={it.key}
                  className="tile"
                  onClick={() => {
                    haptic('light')
                    if (locked) openUpgrade()
                    else navigate(`/c/${cid}/s/${it.key}`)
                  }}
                >
                  <div className={`tile-icon ${!locked && it.on ? 'on' : ''}`}><it.icon size={20} /></div>
                  <div className="tile-body">
                    <div className="tile-title">{it.title}</div>
                    <div className="tile-desc">{it.desc}</div>
                  </div>
                  {locked ? (
                    <span className="badge badge-gold tile-pro"><Lock size={11} /> PRO</span>
                  ) : (
                    <span className={`tile-state ${it.on ? 'on' : ''}`}>
                      {it.state ?? (it.on ? t('dash.enabled') : t('dash.disabled'))}
                    </span>
                  )}
                  <ChevronRight size={16} className="tile-chevron" />
                </motion.button>
              )
            })}
          </div>
        </motion.div>
      ))}
    </div>
  )
}
