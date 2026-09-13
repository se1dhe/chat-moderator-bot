import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { Plus, Lock } from 'lucide-react'
import { useLang } from '../context/LangContext'
import { useChatSettings } from '../context/ChatSettingsContext'
import { Toggle, Row, Segmented, Stepper, Slider, Chips, Spinner } from '../components/ui'
import { haptic, showAlert } from '../lib/telegram'
import { api } from '../lib/api'
import Triggers from './Triggers'

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
    autocomment: <AutoComment s={s} t={t} />,
    triggers: <Triggers chatId={s.cid} t={t} />,
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
      {a.action === 'ban' && (
        <div className="card" style={{ marginTop: '0.75rem' }}>
          <Row title={t('antiflood.banSeconds')}
            value={mins(a.ban_seconds) <= 0 ? t('dur.perm') : `${mins(a.ban_seconds)} ${t('common.minutes')}`}>
            <Stepper value={mins(a.ban_seconds)} min={0} max={7 * 1440} step={60}
              onChange={(v) => s.updateSection('antiflood', { ban_seconds: v * 60 })} />
          </Row>
        </div>
      )}
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
        <Row title="Cross-Chat Blacklist" desc="Instantly ban users who were banned in your other chats.">
          <Toggle checked={m.use_global_bans || false} onChange={(v) => s.updateSection('modes', { use_global_bans: v })} />
        </Row>

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
        onLocked={() => s.openUpgrade()}
        options={[
          { value: 'off', label: t('ai.mode.off') },
          { value: 'quarantine', label: t('ai.mode.quarantine') },
          { value: 'autoban', label: t('ai.mode.autoban'), locked: !s.pro },
        ]} />
      {!s.pro && <div className="row-desc" style={{ margin: '0.5rem 0.2rem 0' }}>{t('pro.autobanNote')}</div>}

      <div className="section-label">AI Provider</div>
      <Segmented value={core.ai_provider || 'ollama'} onChange={(v) => s.updateSection('core', { ai_provider: v })}
        options={[
          { value: 'ollama', label: 'Local (Ollama)' },
          { value: 'openai', label: 'OpenAI' },
          { value: 'gemini', label: 'Gemini' },
          { value: 'claude', label: 'Claude' },
        ]} />
        
      {(core.ai_provider && core.ai_provider !== 'ollama') && (
        <div className="card" style={{ marginTop: '0.75rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          <div style={{ padding: '0.75rem 1rem' }}>
            <div style={{ fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.25rem' }}>API Key {core.ai_has_key && '(Saved)'}</div>
            <input 
              className="input" 
              type="password"
              placeholder={core.ai_has_key ? "••••••••••••••••" : "Enter API Key"}
              onChange={(e) => s.updateSection('core', { ai_api_key: e.target.value })}
              style={{ width: '100%' }}
            />
          </div>
          <div style={{ padding: '0 1rem 0.75rem' }}>
            <div style={{ fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.25rem' }}>Model</div>
            <input 
              className="input" 
              type="text"
              placeholder="e.g. gpt-4o-mini"
              value={core.ai_model || ''}
              onChange={(e) => s.updateSection('core', { ai_model: e.target.value })}
              style={{ width: '100%' }}
            />
          </div>
        </div>
      )}

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
  const locked = !s.pro
  return (
    <>
      {locked && (
        <button className="pro-note" onClick={() => s.openUpgrade()}>
          <Lock size={14} />
          <span>{t('pro.raidNote')}</span>
          <span className="badge badge-gold">PRO</span>
        </button>
      )}
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
          <Toggle checked={r.enabled && !locked} disabled={locked} onDisabledClick={() => s.openUpgrade()}
            onChange={(v) => s.updateSection('raid', { enabled: v })} />
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

// Penalty-duration steppers use minutes; 0 == permanent. Cap at 7 days for the UI.
const DAY_MIN = 1440

function Warns({ s, t }) {
  const core = s.draft.core
  const w = s.draft.warns
  const muteMin = mins(w.mute_seconds)
  const banMin = mins(w.ban_seconds)
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

      {core.warn_action === 'mute' && (
        <div className="card" style={{ marginTop: '0.75rem' }}>
          <Row title={t('warns.muteDuration')} value={muteMin <= 0 ? t('dur.perm') : `${muteMin} ${t('common.minutes')}`}>
            <Stepper value={muteMin} min={0} max={7 * DAY_MIN} step={30}
              onChange={(v) => s.updateSection('warns', { mute_seconds: v * 60 })} />
          </Row>
        </div>
      )}
      {core.warn_action === 'ban' && (
        <div className="card" style={{ marginTop: '0.75rem' }}>
          <Row title={t('warns.banDuration')} value={banMin <= 0 ? t('dur.perm') : `${banMin} ${t('common.minutes')}`}>
            <Stepper value={banMin} min={0} max={7 * DAY_MIN} step={60}
              onChange={(v) => s.updateSection('warns', { ban_seconds: v * 60 })} />
          </Row>
        </div>
      )}
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

function AutoComment({ s, t }) {
  const c = s.draft.auto_comment || { enabled: false, text: '', media_url: '' }
  const [uploading, setUploading] = useState(false)
  
  const handleUpload = async (e) => {
    const file = e.target.files?.[0]
    if (!file) return
    setUploading(true)
    try {
      const { file_id } = await api.uploadMedia(s.chatId, file)
      s.updateSection('auto_comment', { media_url: file_id })
    } catch (err) {
      showAlert(t('common.error') + ': ' + err.message)
    } finally {
      setUploading(false)
      e.target.value = ''
    }
  }

  return (
    <>
      <div className="section-label">{t('sec.autocomment')}</div>
      <div className="card">
        <Row title={t('sec.autocomment.enable')} subtitle={t('sec.autocomment.enable.desc')}>
          <Toggle checked={c.enabled} onChange={(v) => s.updateSection('auto_comment', { enabled: v })} />
        </Row>
      </div>
      
      {c.enabled && (
        <>
          <div className="section-label">{t('sec.autocomment.text')}</div>
          <div className="card p-4">
            <textarea 
              className="w-full bg-transparent border-none outline-none text-[var(--tg-theme-text-color)] resize-none"
              rows={4}
              placeholder={t('sec.autocomment.text.ph')}
              value={c.text}
              onChange={(e) => s.updateSection('auto_comment', { text: e.target.value })}
            />
          </div>
          <div className="section-label">{t('sec.autocomment.media')}</div>
          <div className="card p-4 flex items-center justify-between">
            <div className="text-[13px] text-[var(--tg-theme-hint-color)] truncate mr-3">
              {c.media_url ? t('common.mediaAttached') : t('common.noMedia')}
            </div>
            <label className={`btn btn-secondary px-3 py-1 text-[13px] whitespace-nowrap cursor-pointer ${uploading ? 'opacity-50' : ''}`}>
              {uploading ? t('common.uploading') : t('common.upload')}
              <input type="file" className="hidden" accept="image/*,video/mp4,image/gif" disabled={uploading} onChange={handleUpload} />
            </label>
          </div>
          {c.media_url && (
            <div className="px-4 mt-2 mb-1 text-right">
              <button className="text-[13px] text-red-500" onClick={() => s.updateSection('auto_comment', { media_url: '' })}>
                Remove Media
              </button>
            </div>
          )}
          <p className="px-4 mt-2 text-[13px] text-[var(--tg-theme-hint-color)]">
            {t('sec.autocomment.media.desc')}
          </p>
        </>
      )}
    </>
  )
}
