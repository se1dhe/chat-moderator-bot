import { useState, useEffect } from 'react'
import { Rocket, BrainCircuit, MessageSquare, Filter, Zap, Star } from 'lucide-react'
import { haptic } from '../lib/telegram'
import { useLang } from '../context/LangContext'

const CURRENT_VERSION = 'v2.0.1'

export function WhatsNewModal() {
  const { t } = useLang()
  const [open, setOpen] = useState(false)
  const [slide, setSlide] = useState(0)

  useEffect(() => {
    const seen = localStorage.getItem('seen_whatsnew')
    if (seen !== CURRENT_VERSION) {
      setOpen(true)
    }
  }, [])

  const close = () => {
    haptic('success')
    localStorage.setItem('seen_whatsnew', CURRENT_VERSION)
    setOpen(false)
  }

  const next = () => {
    haptic('light')
    setSlide(s => s + 1)
  }

  if (!open) return null

  const slides = [
    {
      icon: <Rocket size={64} className="text-red-500 mb-6 drop-shadow-[0_0_15px_rgba(239,68,68,0.3)]" />,
      title: t('wn.title.1'),
      desc: t('wn.desc.1'),
      badge: null
    },
    {
      icon: <MessageSquare size={64} className="text-blue-500 mb-6 drop-shadow-[0_0_15px_rgba(59,130,246,0.3)]" />,
      title: t('wn.title.2'),
      desc: t('wn.desc.2'),
      badge: 'PRO'
    },
    {
      icon: <BrainCircuit size={64} className="text-purple-500 mb-6 drop-shadow-[0_0_15px_rgba(168,85,247,0.3)]" />,
      title: t('wn.title.3'),
      desc: t('wn.desc.3'),
      badge: 'PRO'
    },
    {
      icon: <Filter size={64} className="text-green-500 mb-6 drop-shadow-[0_0_15px_rgba(34,197,94,0.3)]" />,
      title: t('wn.title.4'),
      desc: t('wn.desc.4'),
      badge: 'FREE'
    }
  ]

  const current = slides[slide]

  return (
    <div className="fixed inset-0 z-[100] bg-[var(--tg-theme-bg-color)] flex flex-col animate-in fade-in duration-300">
      <div className="flex-1 flex flex-col items-center justify-center p-6 text-center relative overflow-hidden">
        
        {/* Background glow effects */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-[var(--tg-theme-hint-color)] opacity-[0.03] rounded-full blur-3xl pointer-events-none"></div>

        <div className="mb-4">
          {current.badge === 'PRO' && (
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-amber-500/10 text-amber-500 border border-amber-500/20 mb-6">
              <Star size={14} fill="currentColor" /> Pro Feature
            </span>
          )}
          {current.badge === 'FREE' && (
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-green-500/10 text-green-500 border border-green-500/20 mb-6">
              <Zap size={14} fill="currentColor" /> Free
            </span>
          )}
        </div>
        
        <div className="transform transition-all duration-300 scale-100">
          {current.icon}
        </div>
        
        <h2 className="text-3xl font-bold mb-4 text-[var(--tg-theme-text-color)] tracking-tight">
          {current.title}
        </h2>
        
        <p className="text-[var(--tg-theme-hint-color)] mb-8 text-base leading-relaxed max-w-sm">
          {current.desc}
        </p>

        {/* Slide Indicators */}
        <div className="flex gap-2 mb-12">
          {slides.map((_, i) => (
            <div 
              key={i} 
              className={`h-1.5 rounded-full transition-all duration-300 ${i === slide ? 'w-8 bg-red-500' : 'w-2 bg-[var(--tg-theme-hint-color)] opacity-30'}`}
            />
          ))}
        </div>
      </div>

      <div className="p-6 bg-[var(--tg-theme-bg-color)] pb-[max(env(safe-area-inset-bottom),1.5rem)] shadow-[0_-10px_40px_rgba(0,0,0,0.05)]">
        <div className="flex gap-3">
          {slide > 0 && (
            <button className="btn-secondary flex-1 py-4 text-base font-semibold rounded-xl" onClick={() => { haptic('light'); setSlide(s => s - 1) }}>
              {t('wn.btn.back')}
            </button>
          )}
          
          {slide < slides.length - 1 ? (
            <button className="btn flex-[2] py-4 text-base font-semibold rounded-xl bg-red-600 text-white" onClick={next}>
              {t('wn.btn.next')}
            </button>
          ) : (
            <button className="btn flex-[2] py-4 text-base font-semibold rounded-xl bg-red-600 text-white" onClick={close}>
              {t('wn.btn.finish')}
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
