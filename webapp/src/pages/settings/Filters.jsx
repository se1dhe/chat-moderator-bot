import { useState, useEffect, useRef } from 'react'
import { Plus, Lock } from 'lucide-react'
import { Toggle, Row, Segmented, Stepper, Slider, Chips, Spinner } from '../../components/ui'
import { haptic, showAlert } from '../../lib/telegram'
import { api } from '../../lib/api'

export default function Filters({ s, t }) {
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
