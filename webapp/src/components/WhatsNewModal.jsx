import { useState, useEffect } from 'react'
import { Rocket, BrainCircuit, MessageSquare, Filter } from 'lucide-react'
import { haptic } from '../lib/telegram'

const CURRENT_VERSION = 'v2.0.0'

export function WhatsNewModal() {
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
      icon: <Rocket size={48} className="text-red-500 mb-4" />,
      title: 'Welcome to Red Queen 2.0',
      desc: 'We have completely overhauled the system. Enjoy the new interface, better performance, and powerful new features!'
    },
    {
      icon: <MessageSquare size={48} className="text-blue-500 mb-4" />,
      title: 'Auto-Comment',
      desc: 'Automatically post rules or welcome messages as the first comment in discussion groups, with support for media and markdown.'
    },
    {
      icon: <BrainCircuit size={48} className="text-purple-500 mb-4" />,
      title: 'Cloud AI Models',
      desc: 'Bring your own API keys for OpenAI, Gemini, or Claude to unlock cutting-edge moderation precision without relying on local hardware.'
    },
    {
      icon: <Filter size={48} className="text-green-500 mb-4" />,
      title: 'Setup Wizard',
      desc: 'New chats now go through a streamlined onboarding wizard to ensure basic protections are configured right from the start.'
    }
  ]

  const current = slides[slide]

  return (
    <div className="fixed inset-0 z-[100] bg-black/80 flex items-center justify-center p-4 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-[var(--tg-theme-bg-color)] w-full max-w-sm rounded-2xl p-6 flex flex-col items-center text-center shadow-2xl relative">
        <div className="absolute top-4 right-4 text-xs text-[var(--tg-theme-hint-color)]">
          {slide + 1} / {slides.length}
        </div>
        
        <div className="mt-4">{current.icon}</div>
        <h3 className="text-xl font-bold mb-2 text-[var(--tg-theme-text-color)]">{current.title}</h3>
        <p className="text-[var(--tg-theme-hint-color)] mb-8 text-sm leading-relaxed">
          {current.desc}
        </p>

        <div className="w-full flex gap-3">
          {slide > 0 && (
            <button className="btn-secondary flex-1" onClick={() => { haptic('light'); setSlide(s => s - 1) }}>
              Back
            </button>
          )}
          
          {slide < slides.length - 1 ? (
            <button className="btn flex-1" onClick={next}>Next</button>
          ) : (
            <button className="btn flex-1" onClick={close}>Let's go!</button>
          )}
        </div>
      </div>
    </div>
  )
}
