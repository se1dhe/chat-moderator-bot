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

      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('ai.log_channel')}</div>
      <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60 rounded-2xl p-4 mb-4 shadow-sm w-full">
        <div className="text-[13px] font-semibold mb-2">{t('ai.log_channel.desc')}</div>
        <input 
          className="w-full px-4 py-3 bg-neutral-50 dark:bg-black border border-neutral-200 dark:border-neutral-800/60 rounded-xl focus:outline-none focus:border-primary/50 transition-colors font-medium text-[15px]" 
          type="text"
          placeholder="-100..."
          value={s.draft.log_channel_id || ''}
          onChange={(e) => s.setSection('log_channel_id', e.target.value ? Number(e.target.value) : null)}
        />
      </div>

      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('ai.mode')}</div>
      <Segmented value={core.ai_mode} onChange={(v) => s.updateSection('core', { ai_mode: v })}
        onLocked={() => s.openUpgrade()}
        options={[
          { value: 'off', label: t('ai.mode.off') },
          { value: 'quarantine', label: t('ai.mode.quarantine') },
          { value: 'autoban', label: t('ai.mode.autoban'), locked: !s.pro },
        ]} />
      {!s.pro && <div className="text-[13px] text-neutral-500 leading-snug mt-2 mx-1">{t('pro.autobanNote')}</div>}

      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('settings.aiProvider')}</div>
      <Segmented value={core.ai_provider || 'ollama'} onChange={(v) => s.updateSection('core', { ai_provider: v })}
        options={[
          { value: 'ollama', label: t('settings.aiProvider.local') },
          { value: 'openai', label: t('settings.aiProvider.openai') },
          { value: 'gemini', label: t('settings.aiProvider.gemini') },
          { value: 'claude', label: t('settings.aiProvider.claude') },
        ]} />
        
      {(core.ai_provider && core.ai_provider !== 'ollama') && (
        <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60 rounded-2xl p-2 mb-4 shadow-sm w-full mt-3 flex flex-col gap-2">
          <div className="px-4 py-3">
            <div className="text-[13px] font-semibold mb-1">{t('settings.apiKey')} {core.ai_has_key && t('settings.apiKeySaved')}</div>
            <input 
              className="w-full px-4 py-3 bg-neutral-50 dark:bg-black border border-neutral-200 dark:border-neutral-800/60 rounded-xl focus:outline-none focus:border-primary/50 transition-colors font-medium text-[15px]" 
              type="password"
              placeholder={core.ai_has_key ? "••••••••••••••••" : t('settings.enterApiKey')}
              onChange={(e) => s.updateSection('core', { ai_api_key: e.target.value })}
              
            />
          </div>
          <div className="px-4 pb-3">
            <div className="text-[13px] font-semibold mb-1">{t('settings.model')}</div>
            <input 
              className="w-full px-4 py-3 bg-neutral-50 dark:bg-black border border-neutral-200 dark:border-neutral-800/60 rounded-xl focus:outline-none focus:border-primary/50 transition-colors font-medium text-[15px]" 
              type="text"
              placeholder={t('settings.modelPlaceholder')}
              value={core.ai_model || ''}
              onChange={(e) => s.updateSection('core', { ai_model: e.target.value })}
              
            />
          </div>
        </div>
      )}

      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('ai.threshold')} · {core.ai_threshold}%</div>
      <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60 rounded-2xl p-4 mb-4 shadow-sm w-full">
        <Slider value={core.ai_threshold} min={0} max={100} step={5} onChange={(v) => s.updateSection('core', { ai_threshold: v })} />
      </div>

      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('ai.perCategory')}</div>
      <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60 rounded-2xl p-4 mb-4 shadow-sm w-full flex flex-col gap-3">
        {CATEGORIES.map((cat) => {
          const val = ai.thresholds[cat] ?? core.ai_threshold
          const overridden = cat in ai.thresholds
          return (
            <div key={cat}>
              <div className="flex justify-between mb-1.5">
                <span className="font-semibold text-[13px]">{t(`cat.${cat}`)}</span>
                <span className={`text-[13px] ${overridden ? "text-primary" : "text-neutral-500"}`} >
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
      <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60 rounded-2xl p-2 mb-4 shadow-sm w-full">
        <Row title={t('ai.maxPerMinute')} value={ai.max_per_minute}>
          <Stepper value={ai.max_per_minute} min={1} max={600} step={1} onChange={(v) => s.updateSection('ai', { max_per_minute: v })} />
        </Row>
      </div>
    </>
  )
}
