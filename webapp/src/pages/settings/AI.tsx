import { useState, useEffect, useRef } from 'react'
import { Plus, Lock } from 'lucide-react'
import { Toggle, Row, Segmented, Stepper, Slider, Chips, Spinner } from '../../components/ui'
import { haptic, showAlert } from '../../lib/telegram'
import { api } from '../../lib/api'

const CATEGORIES = ['spam', 'scam', 'toxicity', 'nsfw', 'flood']

export default function AI({ s, t }) {
  const ai = s.draft.ai
  const core = s.draft.core
  return (
    <>
      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('ai.mode')}</div>
      <Segmented value={core.ai_mode} onChange={(v) => s.updateSection('core', { ai_mode: v })}
        onLocked={() => s.openUpgrade()}
        options={[
          { value: 'off', label: t('ai.mode.off') },
          { value: 'quarantine', label: t('ai.mode.quarantine') },
          { value: 'autoban', label: t('ai.mode.autoban'), locked: !s.pro },
        ]} />
      {!s.pro && <div className="row-desc" style={{ margin: '0.5rem 0.2rem 0' }}>{t('pro.autobanNote')}</div>}

      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('settings.aiProvider')}</div>
      <Segmented value={core.ai_provider || 'ollama'} onChange={(v) => s.updateSection('core', { ai_provider: v })}
        options={[
          { value: 'ollama', label: t('settings.aiProvider.local') },
          { value: 'openai', label: t('settings.aiProvider.openai') },
          { value: 'gemini', label: t('settings.aiProvider.gemini') },
          { value: 'claude', label: t('settings.aiProvider.claude') },
        ]} />
        
      {(core.ai_provider && core.ai_provider !== 'ollama') && (
        <div className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-2xl p-2 mb-4 shadow-sm w-full" style={{ marginTop: '0.75rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          <div style={{ padding: '0.75rem 1rem' }}>
            <div style={{ fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.25rem' }}>{t('settings.apiKey')} {core.ai_has_key && t('settings.apiKeySaved')}</div>
            <input 
              className="w-full px-4 py-3 bg-neutral-50 dark:bg-neutral-950 border border-neutral-200 dark:border-neutral-800 rounded-xl focus:outline-none focus:border-primary/50 transition-colors font-medium text-[15px]" 
              type="password"
              placeholder={core.ai_has_key ? "••••••••••••••••" : t('settings.enterApiKey')}
              onChange={(e) => s.updateSection('core', { ai_api_key: e.target.value })}
              style={{ width: '100%' }}
            />
          </div>
          <div style={{ padding: '0 1rem 0.75rem' }}>
            <div style={{ fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.25rem' }}>{t('settings.model')}</div>
            <input 
              className="w-full px-4 py-3 bg-neutral-50 dark:bg-neutral-950 border border-neutral-200 dark:border-neutral-800 rounded-xl focus:outline-none focus:border-primary/50 transition-colors font-medium text-[15px]" 
              type="text"
              placeholder={t('settings.modelPlaceholder')}
              value={core.ai_model || ''}
              onChange={(e) => s.updateSection('core', { ai_model: e.target.value })}
              style={{ width: '100%' }}
            />
          </div>
        </div>
      )}

      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('ai.threshold')} · {core.ai_threshold}%</div>
      <div className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-2xl p-4 mb-4 shadow-sm w-full">
        <Slider value={core.ai_threshold} min={0} max={100} step={5} onChange={(v) => s.updateSection('core', { ai_threshold: v })} />
      </div>

      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('ai.perCategory')}</div>
      <div className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-2xl p-4 mb-4 shadow-sm w-full" style={{ display: 'flex', flexDirection: 'column', gap: '0.9rem' }}>
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

      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('ai.maxPerMinute')}</div>
      <div className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-2xl p-2 mb-4 shadow-sm w-full">
        <Row title={t('ai.maxPerMinute')} value={ai.max_per_minute}>
          <Stepper value={ai.max_per_minute} min={1} max={600} step={1} onChange={(v) => s.updateSection('ai', { max_per_minute: v })} />
        </Row>
      </div>
    </>
  )
}
