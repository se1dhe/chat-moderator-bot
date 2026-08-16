import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { Plus, Lock } from 'lucide-react'
import { useLang } from '../context/LangContext'
import { useChatSettings } from '../context/ChatSettingsContext'
import { Toggle, Row, Segmented, Stepper, Slider, Chips, Spinner } from '../components/ui'
import { haptic } from '../lib/telegram'

const CATEGORIES = ['spam', 'scam', 'toxicity', 'nsfw', 'flood']

export function SettingsSection() {
  const { section } = useParams()
  const { t } = useLang()
  const s = useChatSettings()
  if (!s.draft) return <div className="content"><Spinner /></div>

  const map = {
    captcha: <Captcha s={s} t={t} />,
    antiflood: <Antiflood s={s} t={t} />,
    filters: <Filters s={s} t={t} />,
    modes: <Modes s={s} t={t} />,
    ai: <AI s={s} t={t} />,
    raid: <Raid s={s} t={t} />,
    warns: <Warns s={s} t={t} />,
    exempt: <Exempt s={s} t={t} />,
  }
  return <div className="content fade-in">{map[section] ?? null}</div>
}

const mins = (sec) => Math.round(sec / 60)

function Captcha({ s, t }) {
  const c = s.draft.captcha
  return (
    <>
      <div className="section-label">{t('sec.captcha')}</div>
      <div className="card">
        <Row title={t('captcha.enabled')}>
          <Toggle checked={c.enabled} onChange={(v) => s.updateSection('captcha', { enabled: v })} />
        </Row>
        <Row title={t('captcha.timeout')} value={`${mins(c.timeout_seconds)} ${t('common.minutes')}`}>
          <Stepper value={mins(c.timeout_seconds)} min={1} max={30}
            onChange={(v) => s.updateSection('captcha', { timeout_seconds: v * 60 })} />
        </Row>
      </div>
      <div className="section-label">{t('captcha.mode')}</div>
      <Segmented
        value={c.mode}
        onChange={(v) => s.updateSection('captcha', { mode: v })}
        options={[
          { value: 'button', label: t('captcha.mode.button') },
          { value: 'math', label: t('captcha.mode.math') },
        ]}
      />
    </>
  )
}

function Antiflood({ s, t }) {
  const a = s.draft.antiflood
  return (
    <>
      <div className="section-label">{t('sec.antiflood')}</div>
      <div className="card">
        <Row title={t('antiflood.enabled')}>
          <Toggle checked={a.enabled} onChange={(v) => s.updateSection('antiflood', { enabled: v })} />
        </Row>
        <Row title={t('antiflood.limit')} value={a.limit}>
          <Stepper value={a.limit} min={2} max={50} onChange={(v) => s.updateSection('antiflood', { limit: v })} />
        </Row>
        <Row title={t('antiflood.window')} value={`${a.window} ${t('common.seconds')}`}>
          <Stepper value={a.window} min={2} max={300} step={1} onChange={(v) => s.updateSection('antiflood', { window: v })} />
        </Row>
        <Row title={t('antiflood.muteSeconds')} value={`${mins(a.mute_seconds)} ${t('common.minutes')}`}>
          <Stepper value={mins(a.mute_seconds)} min={1} max={1440} onChange={(v) => s.updateSection('antiflood', { mute_seconds: v * 60 })} />
        </Row>
      </div>
      <div className="section-label">{t('antiflood.action')}</div>
      <Segmented value={a.action} onChange={(v) => s.updateSection('antiflood', { action: v })}
        options={[
          { value: 'mute', label: t('action.mute') },
          { value: 'kick', label: t('action.kick') },
          { value: 'ban', label: t('action.ban') },
        ]} />
    </>
  )
}

function Filters({ s, t }) {
  const f = s.draft.filters
  const [word, setWord] = useState('')
  const media = ['sticker', 'animation', 'voice', 'video_note']
  const addWord = () => {
    const w = word.trim().toLowerCase()
    if (w && !f.banned_words.includes(w)) s.updateSection('filters', { banned_words: [...f.banned_words, w] })
    setWord('')
  }
  const toggleMedia = (m) => {
    const has = f.blocked_media.includes(m)
    s.updateSection('filters', { blocked_media: has ? f.blocked_media.filter((x) => x !== m) : [...f.blocked_media, m] })
  }
  return (
    <>
      <div className="section-label">{t('sec.filters')}</div>
      <div className="card">
        <Row title={t('filters.links')}><Toggle checked={f.block_links} onChange={(v) => s.updateSection('filters', { block_links: v })} /></Row>
        <Row title={t('filters.forwards')}><Toggle checked={f.block_forwards} onChange={(v) => s.updateSection('filters', { block_forwards: v })} /></Row>
        <Row title={t('filters.mentions')}><Toggle checked={f.block_mentions} onChange={(v) => s.updateSection('filters', { block_mentions: v })} /></Row>
      </div>

      <div className="section-label">{t('filters.media')}</div>
      <div className="card">
        {media.map((m) => (
          <Row key={m} title={t(`media.${m}`)}>
            <Toggle checked={f.blocked_media.includes(m)} onChange={() => toggleMedia(m)} />
          </Row>
        ))}
      </div>

      <div className="section-label">{t('filters.words')}</div>
      <div className="card card-pad">
        <Chips items={f.banned_words} onRemove={(w) => s.updateSection('filters', { banned_words: f.banned_words.filter((x) => x !== w) })} />
        <div className="chip-input">
          <input className="input" value={word} placeholder={t('filters.wordsPlaceholder')}
            onChange={(e) => setWord(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && addWord()} />
          <button className="btn btn-primary" onClick={addWord}><Plus size={16} /></button>
        </div>
      </div>
    </>
  )
}

function Modes({ s, t }) {
  const m = s.draft.modes
  return (
    <>
      <div className="section-label">{t('modes.night')}</div>
      <div className="card">
        <Row title={t('modes.night')}>
          <Toggle checked={m.night.enabled} onChange={(v) => s.updateSection('modes', { night: { ...m.night, enabled: v } })} />
        </Row>
        <Row title={t('modes.nightRange')} value={`${m.night.start}:00 – ${m.night.end}:00`}>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <Stepper value={m.night.start} min={0} max={23} onChange={(v) => s.updateSection('modes', { night: { ...m.night, start: v } })} />
            <Stepper value={m.night.end} min={0} max={23} onChange={(v) => s.updateSection('modes', { night: { ...m.night, end: v } })} />
          </div>
        </Row>
      </div>
      <div className="card">
        <Row title={t('modes.silent')} desc={t('modes.silentDesc')}>
          <Toggle checked={m.silent} onChange={(v) => s.updateSection('modes', { silent: v })} />
        </Row>
        <Row title={t('modes.slow')} desc={t('modes.slowDesc')} value={`${m.slow_seconds} ${t('common.seconds')}`}>
          <Stepper value={m.slow_seconds} min={0} max={3600} step={5} onChange={(v) => s.updateSection('modes', { slow_seconds: v })} />
        </Row>
      </div>
    </>
  )
}

function AI({ s, t }) {
  const ai = s.draft.ai
  const core = s.draft.core
  return (
    <>
      <div className="section-label">{t('ai.mode')}</div>
      <Segmented value={core.ai_mode} onChange={(v) => s.updateSection('core', { ai_mode: v })}
        options={[
          { value: 'off', label: t('ai.mode.off') },
          { value: 'quarantine', label: t('ai.mode.quarantine') },
          { value: 'autoban', label: t('ai.mode.autoban') },
        ]} />

      <div className="section-label">{t('ai.threshold')} · {core.ai_threshold}%</div>
      <div className="card card-pad">
        <Slider value={core.ai_threshold} min={0} max={100} step={5} onChange={(v) => s.updateSection('core', { ai_threshold: v })} />
      </div>

      <div className="section-label">{t('ai.perCategory')}</div>
      <div className="card card-pad" style={{ display: 'flex', flexDirection: 'column', gap: '0.9rem' }}>
        {CATEGORIES.map((cat) => {
          const val = ai.thresholds[cat] ?? core.ai_threshold
          const overridden = cat in ai.thresholds
          return (
            <div key={cat}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.35rem' }}>
                <span style={{ fontWeight: 600, fontSize: '0.85rem' }}>{t(`cat.${cat}`)}</span>
                <span className={`row-value ${overridden ? '' : ''}`} style={{ color: overridden ? 'var(--primary-light)' : 'var(--text-muted)' }}>
                  {val}%{overridden ? '' : ` · ${t('ai.threshold')}`}
                </span>
              </div>
              <Slider value={val} min={0} max={100} step={5}
                onChange={(v) => s.updateSection('ai', { thresholds: { ...ai.thresholds, [cat]: v } })} />
            </div>
          )
        })}
      </div>

      <div className="section-label">{t('ai.maxPerMinute')}</div>
      <div className="card">
        <Row title={t('ai.maxPerMinute')} value={ai.max_per_minute}>
          <Stepper value={ai.max_per_minute} min={1} max={600} step={1} onChange={(v) => s.updateSection('ai', { max_per_minute: v })} />
        </Row>
      </div>
    </>
  )
}

function Raid({ s, t }) {
  const r = s.draft.raid
  return (
    <>
      {r.locked && (
        <div className="card card-pad" style={{ display: 'flex', alignItems: 'center', gap: '0.7rem' }}>
          <span className="badge badge-danger"><Lock size={12} /> {t('raid.locked')}</span>
          <div className="header-spacer" />
          <button className="btn btn-danger" onClick={() => { haptic('warning'); s.updateSection('raid', { locked: false }) }}>
            {t('raid.unlock')}
          </button>
        </div>
      )}
      <div className="section-label">{t('sec.raid')}</div>
      <div className="card">
        <Row title={t('raid.enabled')}>
          <Toggle checked={r.enabled} onChange={(v) => s.updateSection('raid', { enabled: v })} />
        </Row>
        <Row title={t('raid.threshold')} value={r.join_threshold}>
          <Stepper value={r.join_threshold} min={2} max={100} onChange={(v) => s.updateSection('raid', { join_threshold: v })} />
        </Row>
        <Row title={t('raid.window')} value={`${r.window_seconds} ${t('common.seconds')}`}>
          <Stepper value={r.window_seconds} min={5} max={600} step={5} onChange={(v) => s.updateSection('raid', { window_seconds: v })} />
        </Row>
        <Row title={t('raid.lock')} value={`${mins(r.lock_seconds)} ${t('common.minutes')}`}>
          <Stepper value={mins(r.lock_seconds)} min={1} max={1440} onChange={(v) => s.updateSection('raid', { lock_seconds: v * 60 })} />
        </Row>
      </div>
    </>
  )
}

function Warns({ s, t }) {
  const core = s.draft.core
  return (
    <>
      <div className="section-label">{t('sec.warns')}</div>
      <div className="card">
        <Row title={t('warns.limit')} value={core.warn_limit}>
          <Stepper value={core.warn_limit} min={1} max={20} onChange={(v) => s.updateSection('core', { warn_limit: v })} />
        </Row>
      </div>
      <div className="section-label">{t('warns.action')}</div>
      <Segmented value={core.warn_action} onChange={(v) => s.updateSection('core', { warn_action: v })}
        options={[
          { value: 'mute', label: t('action.mute') },
          { value: 'kick', label: t('action.kick') },
          { value: 'ban', label: t('action.ban') },
        ]} />
    </>
  )
}

function Exempt({ s, t }) {
  const ids = s.draft.exempt_user_ids
  const [val, setVal] = useState('')
  const add = () => {
    const n = parseInt(val.trim(), 10)
    if (Number.isFinite(n) && !ids.includes(n)) s.setSection('exempt_user_ids', [...ids, n])
    setVal('')
  }
  return (
    <>
      <div className="section-label">{t('sec.exempt')}</div>
      <div className="card card-pad">
        {ids.length ? (
          <Chips items={ids.map(String)} onRemove={(x) => s.setSection('exempt_user_ids', ids.filter((i) => String(i) !== x))} />
        ) : (
          <div className="row-desc">{t('exempt.empty')}</div>
        )}
        <div className="chip-input">
          <input className="input" inputMode="numeric" value={val} placeholder={t('exempt.add')}
            onChange={(e) => setVal(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && add()} />
          <button className="btn btn-primary" onClick={add}><Plus size={16} /></button>
        </div>
      </div>
    </>
  )
}
