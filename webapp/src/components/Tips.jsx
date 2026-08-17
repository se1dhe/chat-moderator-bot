import { useEffect, useState } from 'react'
import { Lightbulb, ShieldCheck } from 'lucide-react'
import { useLang } from '../context/LangContext'
import { useChatSettings } from '../context/ChatSettingsContext'
import { api } from '../lib/api'

// Contextual recommendations derived from the chat's own configuration + activity.
function buildTips(d, stats) {
  const tips = []
  const f = d.filters
  if (!d.captcha.enabled) tips.push('tips.captcha')
  if (!d.antiflood.enabled) tips.push('tips.antiflood')
  if (d.core.ai_mode === 'off') tips.push('tips.ai')
  else tips.push(null) // ai on → maybe vision hint handled below
  if (!d.raid.enabled) tips.push('tips.raid')
  if (!f.block_links && f.banned_words.length === 0 && f.blocked_media.length === 0) tips.push('tips.filters')
  if (stats && stats.pending_quarantine > 0) tips.push('tips.quarantine')
  return tips.filter(Boolean)
}

export function Tips({ chatId }) {
  const { t } = useLang()
  const { draft } = useChatSettings()
  const [stats, setStats] = useState(null)

  useEffect(() => { api.stats(chatId).then(setStats).catch(() => setStats(null)) }, [chatId])

  if (!draft) return null
  const tips = buildTips(draft, stats).slice(0, 3)

  return (
    <>
      <div className="section-label">{t('tips.title')}</div>
      {tips.length === 0 ? (
        <div className="tip tip--ok"><ShieldCheck size={16} /><span>{t('tips.allGood')}</span></div>
      ) : (
        tips.map((k) => (
          <div className="tip" key={k}><Lightbulb size={16} /><span>{t(k)}</span></div>
        ))
      )}
    </>
  )
}
