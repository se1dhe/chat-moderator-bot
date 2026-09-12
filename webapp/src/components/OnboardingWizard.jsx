import { useState } from 'react'
import { ShieldCheck, Moon, Filter, Check, Rocket } from 'lucide-react'
import { useLang } from '../context/LangContext'
import { useChatSettings } from '../context/ChatSettingsContext'
import { haptic } from '../lib/telegram'
import { Toggle, Row, Spinner } from './ui'

export function OnboardingWizard() {
  const { t } = useLang()
  const { draft, setSection, updateSection, pro, openUpgrade, billing } = useChatSettings()
  const [step, setStep] = useState(1)
  
  if (!draft) return <Spinner />

  const next = () => {
    haptic('light')
    setStep(s => s + 1)
  }
  
  const finish = () => {
    haptic('success')
    updateSection('onboarding', { setup_completed: true })
  }

  const s1 = (
    <div className="center-state fade-in">
      <div className="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mb-4">
        <Rocket size={32} className="text-red-500" />
      </div>
      <h3>Welcome to Red Queen</h3>
      <p className="text-sm text-[var(--tg-theme-hint-color)] mb-6 text-center">
        Let's configure the defense protocols for your group.
      </p>
      
      <div className="card w-full text-left mb-6">
        <Row title="Basic Protection" subtitle="Anti-flood & Captcha">
          <Toggle checked={draft.antiflood.enabled} onChange={v => updateSection('antiflood', { enabled: v })} />
        </Row>
      </div>

      <button className="btn" onClick={next}>Continue</button>
    </div>
  )

  const s2 = (
    <div className="center-state fade-in">
      <div className="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mb-4">
        <Filter size={32} className="text-red-500" />
      </div>
      <h3>Content Moderation</h3>
      <p className="text-sm text-[var(--tg-theme-hint-color)] mb-6 text-center">
        Enable AI review and content filters to keep the chat clean.
      </p>
      
      <div className="card w-full text-left mb-6">
        <Row title="AI Moderation" subtitle="Scan messages using AI">
          <Toggle checked={draft.core.ai_mode !== 'off'} onChange={v => updateSection('core', { ai_mode: v ? 'quarantine' : 'off' })} />
        </Row>
        <Row title="Block links" subtitle="Prevent unauthorized links">
          <Toggle checked={draft.filters.block_links} onChange={v => updateSection('filters', { block_links: v })} />
        </Row>
      </div>

      <button className="btn" onClick={next}>Continue</button>
    </div>
  )

  const s3 = (
    <div className="center-state fade-in">
      <div className="w-16 h-16 bg-yellow-500/20 rounded-full flex items-center justify-center mb-4">
        <ShieldCheck size={32} className="text-yellow-500" />
      </div>
      <h3>Unlock Pro</h3>
      <p className="text-sm text-[var(--tg-theme-hint-color)] mb-6 text-center">
        Upgrade to unlock Raid Shield, Auto-Comment, custom AI models, and unlimited AI scans.
      </p>
      
      {!pro ? (
        <>
          <button className="btn w-full mb-4" style={{ background: '#f59e0b', color: '#fff' }} onClick={openUpgrade}>
            Unlock Pro for {billing?.price_stars || 500} Stars
          </button>
          <button className="btn-secondary w-full" onClick={finish}>Skip for now</button>
        </>
      ) : (
        <>
          <div className="text-green-500 font-medium mb-4 flex items-center gap-2">
            <Check size={20} /> Pro Unlocked!
          </div>
          <button className="btn w-full" onClick={finish}>Finish Setup</button>
        </>
      )}
    </div>
  )

  return (
    <div className="content">
      {step === 1 && s1}
      {step === 2 && s2}
      {step === 3 && s3}
    </div>
  )
}
