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
      icon: <Rocket size={64} color="#ef4444" style={{ marginBottom: 24, filter: 'drop-shadow(0 0 15px rgba(239,68,68,0.3))' }} />,
      title: t('wn.title.1'),
      desc: t('wn.desc.1'),
      badge: null
    },
    {
      icon: <MessageSquare size={64} color="#3b82f6" style={{ marginBottom: 24, filter: 'drop-shadow(0 0 15px rgba(59,130,246,0.3))' }} />,
      title: t('wn.title.2'),
      desc: t('wn.desc.2'),
      badge: 'PRO'
    },
    {
      icon: <BrainCircuit size={64} color="#a855f7" style={{ marginBottom: 24, filter: 'drop-shadow(0 0 15px rgba(168,85,247,0.3))' }} />,
      title: t('wn.title.3'),
      desc: t('wn.desc.3'),
      badge: 'PRO'
    },
    {
      icon: <Filter size={64} color="#22c55e" style={{ marginBottom: 24, filter: 'drop-shadow(0 0 15px rgba(34,197,94,0.3))' }} />,
      title: t('wn.title.4'),
      desc: t('wn.desc.4'),
      badge: 'FREE'
    }
  ]

  const current = slides[slide]

  return (
    <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, zIndex: 100, backgroundColor: 'var(--tg-theme-bg-color, #000)', display: 'flex', flexDirection: 'column' }}>
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '24px', textAlign: 'center', position: 'relative', overflow: 'hidden' }}>
        
        <div style={{ marginBottom: 16 }}>
          {current.badge === 'PRO' && (
            <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6, padding: '4px 12px', borderRadius: 99, fontSize: 12, fontWeight: 'bold', textTransform: 'uppercase', background: 'rgba(245,158,11,0.1)', color: '#f59e0b', border: '1px solid rgba(245,158,11,0.2)', marginBottom: 24 }}>
              <Star size={14} fill="currentColor" /> Pro Feature
            </span>
          )}
          {current.badge === 'FREE' && (
            <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6, padding: '4px 12px', borderRadius: 99, fontSize: 12, fontWeight: 'bold', textTransform: 'uppercase', background: 'rgba(34,197,94,0.1)', color: '#22c55e', border: '1px solid rgba(34,197,94,0.2)', marginBottom: 24 }}>
              <Zap size={14} fill="currentColor" /> Free
            </span>
          )}
        </div>
        
        <div>
          {current.icon}
        </div>
        
        <h2 style={{ fontSize: '1.75rem', fontWeight: 700, marginBottom: 16, color: 'var(--tg-theme-text-color)' }}>
          {current.title}
        </h2>
        
        <p style={{ color: 'var(--tg-theme-hint-color)', marginBottom: 32, fontSize: '1rem', lineHeight: 1.5, maxWidth: 320 }}>
          {current.desc}
        </p>

        {/* Slide Indicators */}
        <div style={{ display: 'flex', gap: 8, marginBottom: 48 }}>
          {slides.map((_, i) => (
            <div 
              key={i} 
              style={{ height: 6, borderRadius: 99, transition: 'all 0.3s', width: i === slide ? 32 : 8, backgroundColor: i === slide ? '#ef4444' : 'var(--tg-theme-hint-color)', opacity: i === slide ? 1 : 0.3 }}
            />
          ))}
        </div>
      </div>

      <div style={{ padding: '24px', backgroundColor: 'var(--tg-theme-bg-color)', paddingBottom: 'max(env(safe-area-inset-bottom), 24px)', boxShadow: '0 -10px 40px rgba(0,0,0,0.05)' }}>
        <div style={{ display: 'flex', gap: 12 }}>
          {slide > 0 && (
            <button className="btn" style={{ flex: 1, padding: '16px', fontSize: '1rem', background: 'transparent', border: '1px solid var(--border)' }} onClick={() => { haptic('light'); setSlide(s => s - 1) }}>
              {t('wn.btn.back')}
            </button>
          )}
          
          {slide < slides.length - 1 ? (
            <button className="btn btn-primary" style={{ flex: 2, padding: '16px', fontSize: '1rem' }} onClick={next}>
              {t('wn.btn.next')}
            </button>
          ) : (
            <button className="btn btn-primary" style={{ flex: 2, padding: '16px', fontSize: '1rem' }} onClick={close}>
              {t('wn.btn.finish')}
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
