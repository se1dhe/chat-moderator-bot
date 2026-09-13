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
      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('sec.filters')}</div>
      <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60/60/60/60 rounded-2xl p-2 mb-4 shadow-sm w-full">
        <Row title={t('filters.links')}><Toggle checked={f.block_links} onChange={(v) => s.updateSection('filters', { block_links: v })} /></Row>
        <Row title={t('filters.forwards')}><Toggle checked={f.block_forwards} onChange={(v) => s.updateSection('filters', { block_forwards: v })} /></Row>
        <Row title={t('filters.mentions')}><Toggle checked={f.block_mentions} onChange={(v) => s.updateSection('filters', { block_mentions: v })} /></Row>
      </div>

      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('filters.media')}</div>
      <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60/60/60/60 rounded-2xl p-2 mb-4 shadow-sm w-full">
        {media.map((m) => (
          <Row key={m} title={t(`media.${m}`)}>
            <Toggle checked={f.blocked_media.includes(m)} onChange={() => toggleMedia(m)} />
          </Row>
        ))}
      </div>

      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('filters.words')}</div>
      <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60/60/60/60 rounded-2xl p-4 mb-4 shadow-sm w-full">
        <Chips items={f.banned_words} onRemove={(w) => s.updateSection('filters', { banned_words: f.banned_words.filter((x) => x !== w) })} />
        <div className="chip-input">
          <input className="w-full px-4 py-3 bg-neutral-50 dark:bg-black border border-neutral-200 dark:border-neutral-800/60/60/60/60 rounded-xl focus:outline-none focus:border-primary/50 transition-colors font-medium text-[15px]" value={word} placeholder={t('filters.wordsPlaceholder')}
            onChange={(e) => setWord(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && addWord()} />
          <button className="w-full flex items-center justify-center gap-2 py-3 bg-gradient-to-r from-red-600 to-red-500 hover:from-red-500 hover:to-red-400 text-white shadow-[0_4px_20px_-4px_rgba(220,38,38,0.5)] rounded-xl font-bold transition-all active:scale-95  text-[15px]" onClick={addWord}><Plus size={16} /></button>
        </div>
      </div>
    </>
  )
}
