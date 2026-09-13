import { useState, useEffect } from 'react';
import { Rocket, BrainCircuit, MessageSquare, Filter, Zap, Star } from 'lucide-react';
import { haptic } from '../lib/telegram';
import { useLang } from '../context/LangContext';

const CURRENT_VERSION = 'v2.0.1';

export function WhatsNewModal() {
  const { t } = useLang();
  const [open, setOpen] = useState(false);
  const [slide, setSlide] = useState(0);

  useEffect(() => {
    const seen = localStorage.getItem('seen_whatsnew');
    if (seen !== CURRENT_VERSION) {
      setOpen(true);
    }
  }, []);

  const close = () => {
    haptic('success');
    localStorage.setItem('seen_whatsnew', CURRENT_VERSION);
    setOpen(false);
  };

  const next = () => {
    haptic('light');
    setSlide(s => s + 1);
  };

  if (!open) return null;

  const slides = [
    {
      icon: <Rocket size={64} className="text-primary mb-6 drop-shadow-[0_0_15px_rgba(239,68,68,0.3)]" />,
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
      icon: <Filter size={64} className="text-emerald-500 mb-6 drop-shadow-[0_0_15px_rgba(34,197,94,0.3)]" />,
      title: t('wn.title.4'),
      desc: t('wn.desc.4'),
      badge: 'FREE'
    }
  ];

  const current = slides[slide];

  return (
    <div className="fixed inset-0 z-[100] bg-neutral-50 dark:bg-black flex flex-col animate-in fade-in duration-300">
      <div className="flex-1 flex flex-col items-center justify-center p-6 text-center relative overflow-hidden">
        
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-primary/5 rounded-full blur-3xl pointer-events-none"></div>

        <div className="mb-4">
          {current.badge === 'PRO' && (
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-amber-500/10 text-amber-600 border border-amber-500/20 mb-6">
              <Star size={14} fill="currentColor" /> Pro Feature
            </span>
          )}
          {current.badge === 'FREE' && (
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-emerald-500/10 text-emerald-600 border border-emerald-500/20 mb-6">
              <Zap size={14} fill="currentColor" /> Free
            </span>
          )}
        </div>
        
        <div className="transform transition-all duration-300 scale-100">
          {current.icon}
        </div>
        
        <h2 className="text-3xl font-black mb-4 text-neutral-900 dark:text-neutral-50 tracking-tight">
          {current.title}
        </h2>
        
        <p className="text-neutral-500 mb-8 text-base leading-relaxed max-w-[280px]">
          {current.desc}
        </p>

        <div className="flex gap-2 mb-12">
          {slides.map((_, i) => (
            <div 
              key={i} 
              className={`h-1.5 rounded-full transition-all duration-300 ${i === slide ? 'w-8 bg-primary' : 'w-2 bg-neutral-300 dark:bg-neutral-700'}`}
            />
          ))}
        </div>
      </div>

      <div className="p-4 bg-white/80 dark:bg-black/70 backdrop-blur-xl pb-safe border-t border-neutral-200 dark:border-neutral-800/60">
        <div className="flex gap-3 max-w-md mx-auto">
          {slide > 0 && (
            <button 
              className="flex-1 py-3.5 text-base font-bold rounded-xl bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 transition-colors active:bg-neutral-200 dark:active:bg-neutral-700" 
              onClick={() => { haptic('light'); setSlide(s => s - 1); }}
            >
              {t('wn.btn.back')}
            </button>
          )}
          
          {slide < slides.length - 1 ? (
            <button 
              className="flex-[2] py-3.5 text-base font-bold rounded-xl bg-primary text-white shadow-lg shadow-primary/20 transition-all active:scale-95" 
              onClick={next}
            >
              {t('wn.btn.next')}
            </button>
          ) : (
            <button 
              className="flex-[2] py-3.5 text-base font-bold rounded-xl bg-primary text-white shadow-lg shadow-primary/20 transition-all active:scale-95" 
              onClick={close}
            >
              {t('wn.btn.finish')}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
