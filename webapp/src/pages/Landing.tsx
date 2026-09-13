import { useState, useEffect } from 'react';
import { ShieldCheck, Zap, Activity, Check, Menu, X, ArrowRight, Bot, Lock, Eye, Sparkles } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useLang } from '../context/LangContext';
import { api } from '../lib/api';
import { LiveFeed } from '../components/LiveFeed';
import { ThemeToggle } from '../components/ThemeToggle';
import { LanguageSwitcher } from '../components/LanguageSwitcher';

const fadeIn = {
  initial: { opacity: 0, y: 20 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true, margin: "-100px" }
};

export function Landing() {
  const { t } = useLang();
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenu, setMobileMenu] = useState(false);
  const [stats, setStats] = useState({ total_actions: 0, protected_chats: 0, ai_decisions: 0 });

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    api.get<any>('/stats/global')
      .then((res) => setStats({
        total_actions: res.mod_actions || 0,
        protected_chats: res.chats || 0,
        ai_decisions: res.ai_verdicts || 0
      }))
      .catch(() => {});
  }, []);

  const navLinks = [
    { href: '#features', label: t('landing.nav.features') },
    { href: '#live', label: t('landing.nav.live') },
    { href: '#pricing', label: t('landing.nav.pricing') },
  ];

  return (
    <div className="min-h-screen bg-[#fafafa] dark:bg-black text-neutral-900 dark:text-neutral-50 font-sans selection:bg-primary/20 overflow-hidden">
      
      {/* Premium Background Effects */}
      <div className="fixed inset-0 pointer-events-none z-0">
        <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] rounded-full bg-primary/10 dark:bg-primary/5 blur-[120px]" />
        <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] rounded-full bg-blue-500/10 dark:bg-blue-500/5 blur-[120px]" />
      </div>

      {/* Header */}
      <header className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${scrolled ? 'bg-white/70 dark:bg-black/60 backdrop-blur-2xl shadow-[0_1px_2px_rgba(0,0,0,0.05)] dark:shadow-[0_1px_2px_rgba(255,255,255,0.02)] py-4' : 'bg-transparent py-6'}`}>
        <div className="max-w-7xl mx-auto px-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="relative flex items-center justify-center w-9 h-9 rounded-xl bg-gradient-to-br from-primary to-primary/80 shadow-lg shadow-primary/20">
              <ShieldCheck className="text-white w-5 h-5" />
            </div>
            <span className="font-extrabold text-xl tracking-tight">RedQueen</span>
          </div>

          {/* Desktop Nav */}
          <nav className="hidden md:flex items-center gap-8">
            {navLinks.map(l => (
              <a key={l.href} href={l.href} className="text-sm font-semibold text-neutral-600 dark:text-neutral-400 hover:text-primary dark:hover:text-primary transition-colors">
                {l.label}
              </a>
            ))}
          </nav>

          <div className="hidden md:flex items-center gap-3">
            <LanguageSwitcher />
            <ThemeToggle />
            <a href="https://t.me/se1dhe_bot" className="ml-2 flex items-center gap-2 px-5 py-2.5 rounded-xl font-bold text-sm bg-neutral-900 dark:bg-white text-white dark:text-black hover:bg-neutral-800 dark:hover:bg-neutral-200 transition-colors">
              {t('landing.nav.login')}
            </a>
          </div>

          {/* Mobile Toggle */}
          <div className="flex md:hidden items-center gap-2">
            <LanguageSwitcher />
            <button className="p-2" onClick={() => setMobileMenu(!mobileMenu)}>
              {mobileMenu ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </header>

      {/* Mobile Menu */}
      <AnimatePresence>
        {mobileMenu && (
          <motion.div 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="fixed inset-0 z-40 bg-white/95 dark:bg-black/95 backdrop-blur-3xl pt-24 px-6 flex flex-col md:hidden"
          >
            <nav className="flex flex-col gap-6 text-2xl font-bold">
              {navLinks.map(l => (
                <a key={l.href} href={l.href} onClick={() => setMobileMenu(false)} className="text-neutral-900 dark:text-white border-b border-neutral-200 dark:border-neutral-800/50 pb-4">
                  {l.label}
                </a>
              ))}
              <div className="flex items-center justify-between py-4 border-b border-neutral-200 dark:border-neutral-800/50">
                <span>Theme</span>
                <ThemeToggle />
              </div>
              <a href="https://t.me/se1dhe_bot" className="mt-8 flex items-center justify-center gap-2 px-6 py-4 rounded-2xl font-bold text-lg bg-primary text-white">
                {t('landing.nav.login')}
              </a>
            </nav>
          </motion.div>
        )}
      </AnimatePresence>

      <main className="pt-32 relative z-10">
        
        {/* Hero */}
        <section className="px-6 pb-20 pt-10 md:pt-20 max-w-5xl mx-auto text-center">
          <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8, ease: "easeOut" }} className="flex flex-col items-center">
            
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary font-bold text-sm mb-8 ring-1 ring-primary/20">
              <Sparkles size={16} />
              {t('landing.hero.badge')}
            </div>

            <h1 className="text-5xl md:text-7xl font-black tracking-tight mb-8 leading-[1.1]">
              {t('landing.hero.title1')}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-500 to-teal-400">{t('landing.hero.title_safe')}</span>
              {t('landing.hero.title2')}
              <br className="hidden md:block" />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-amber-500">{t('landing.hero.title_clean')}</span>
            </h1>
            
            <p className="text-xl md:text-2xl text-neutral-500 max-w-3xl mx-auto mb-12 leading-relaxed">
              {t('landing.hero.desc')}
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 items-center justify-center w-full sm:w-auto">
              <a href="https://t.me/se1dhe_bot" className="w-full sm:w-auto flex items-center justify-center gap-2 px-8 py-4 rounded-2xl font-bold text-lg bg-primary hover:bg-primary/90 text-white shadow-xl shadow-primary/25 transition-all hover:scale-105 active:scale-95">
                {t('landing.hero.cta')} <ArrowRight size={20} />
              </a>
              <a href="#live" className="w-full sm:w-auto flex items-center justify-center gap-2 px-8 py-4 rounded-2xl font-bold text-lg bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 hover:bg-neutral-50 dark:hover:bg-neutral-800 transition-colors">
                <Activity size={20} /> {t('landing.hero.demo')}
              </a>
            </div>

          </motion.div>
        </section>

        {/* Premium Stats Strip */}
        <section className="border-y border-neutral-200 dark:border-neutral-800/60 bg-white/50 dark:bg-black/20 backdrop-blur-md">
          <div className="max-w-7xl mx-auto px-6 py-12">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center divide-y md:divide-y-0 md:divide-x divide-neutral-200 dark:divide-neutral-800/60">
              <motion.div {...fadeIn} transition={{ delay: 0.1 }} className="flex flex-col items-center pt-8 md:pt-0">
                <div className="text-4xl md:text-5xl font-black text-neutral-900 dark:text-white mb-2 font-mono">
                  {(stats.protected_chats / 1000).toFixed(1)}K+
                </div>
                <div className="text-sm font-bold text-neutral-500 uppercase tracking-widest">{t('landing.stats.chats')}</div>
              </motion.div>
              <motion.div {...fadeIn} transition={{ delay: 0.2 }} className="flex flex-col items-center pt-8 md:pt-0">
                <div className="text-4xl md:text-5xl font-black text-neutral-900 dark:text-white mb-2 font-mono">
                  {(stats.total_actions / 1000).toFixed(1)}K+
                </div>
                <div className="text-sm font-bold text-neutral-500 uppercase tracking-widest">{t('landing.stats.actions')}</div>
              </motion.div>
              <motion.div {...fadeIn} transition={{ delay: 0.3 }} className="flex flex-col items-center pt-8 md:pt-0">
                <div className="text-4xl md:text-5xl font-black text-primary mb-2 font-mono">
                  {stats.ai_decisions.toLocaleString()}
                </div>
                <div className="text-sm font-bold text-primary uppercase tracking-widest">{t('landing.stats.ai')}</div>
              </motion.div>
            </div>
          </div>
        </section>

        {/* Bento Features */}
        <section id="features" className="px-6 py-32 max-w-7xl mx-auto">
          <motion.div {...fadeIn} className="text-center mb-20">
            <h3 className="text-4xl md:text-5xl font-black tracking-tight mb-6">{t('landing.features.title')}</h3>
            <p className="text-xl text-neutral-500 max-w-2xl mx-auto">{t('landing.features.desc')}</p>
          </motion.div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Bento 1: Large */}
            <motion.div {...fadeIn} transition={{ delay: 0.1 }} className="md:col-span-2 bg-gradient-to-br from-neutral-100 to-white dark:from-[#111] dark:to-[#0a0a0a] p-8 md:p-12 rounded-[2.5rem] border border-neutral-200 dark:border-neutral-800/60 shadow-sm relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-64 h-64 bg-primary/10 rounded-full blur-[80px] -mr-20 -mt-20 transition-transform group-hover:scale-110" />
              <div className="w-16 h-16 bg-white dark:bg-black shadow-lg rounded-2xl flex items-center justify-center mb-8 relative z-10 border border-neutral-100 dark:border-neutral-800">
                <Bot size={32} className="text-primary" />
              </div>
              <h4 className="text-3xl font-bold mb-4 text-neutral-900 dark:text-white relative z-10">{t('landing.feat1.title')}</h4>
              <p className="text-lg text-neutral-500 leading-relaxed max-w-md relative z-10">{t('landing.feat1.desc')}</p>
            </motion.div>

            {/* Bento 2 */}
            <motion.div {...fadeIn} transition={{ delay: 0.2 }} className="bg-gradient-to-br from-neutral-100 to-white dark:from-[#111] dark:to-[#0a0a0a] p-8 md:p-10 rounded-[2.5rem] border border-neutral-200 dark:border-neutral-800/60 shadow-sm flex flex-col justify-end">
              <div className="w-14 h-14 bg-white dark:bg-black shadow-lg rounded-2xl flex items-center justify-center mb-6 border border-neutral-100 dark:border-neutral-800">
                <Lock size={28} className="text-emerald-500" />
              </div>
              <h4 className="text-2xl font-bold mb-3 text-neutral-900 dark:text-white">{t('landing.feat2.title')}</h4>
              <p className="text-neutral-500 leading-relaxed">{t('landing.feat2.desc')}</p>
            </motion.div>

            {/* Bento 3 */}
            <motion.div {...fadeIn} transition={{ delay: 0.3 }} className="bg-gradient-to-br from-neutral-100 to-white dark:from-[#111] dark:to-[#0a0a0a] p-8 md:p-10 rounded-[2.5rem] border border-neutral-200 dark:border-neutral-800/60 shadow-sm flex flex-col justify-end">
              <div className="w-14 h-14 bg-white dark:bg-black shadow-lg rounded-2xl flex items-center justify-center mb-6 border border-neutral-100 dark:border-neutral-800">
                <Eye size={28} className="text-blue-500" />
              </div>
              <h4 className="text-2xl font-bold mb-3 text-neutral-900 dark:text-white">{t('landing.feat4.title')}</h4>
              <p className="text-neutral-500 leading-relaxed">{t('landing.feat4.desc')}</p>
            </motion.div>

            {/* Bento 4: Large */}
            <motion.div {...fadeIn} transition={{ delay: 0.4 }} className="md:col-span-2 bg-gradient-to-br from-neutral-100 to-white dark:from-[#111] dark:to-[#0a0a0a] p-8 md:p-12 rounded-[2.5rem] border border-neutral-200 dark:border-neutral-800/60 shadow-sm relative overflow-hidden group">
              <div className="absolute bottom-0 right-0 w-80 h-80 bg-blue-500/10 rounded-full blur-[80px] -mr-20 -mb-20 transition-transform group-hover:scale-110" />
              <div className="w-16 h-16 bg-white dark:bg-black shadow-lg rounded-2xl flex items-center justify-center mb-8 relative z-10 border border-neutral-100 dark:border-neutral-800">
                <Activity size={32} className="text-blue-500" />
              </div>
              <h4 className="text-3xl font-bold mb-4 text-neutral-900 dark:text-white relative z-10">{t('landing.feat3.title')}</h4>
              <p className="text-lg text-neutral-500 leading-relaxed max-w-md relative z-10">{t('landing.feat3.desc')}</p>
            </motion.div>
          </div>
        </section>

        {/* Live Feed */}
        <section id="live" className="px-6 py-32 bg-neutral-900 dark:bg-[#050505] text-white">
          <div className="max-w-5xl mx-auto">
            <motion.div {...fadeIn} className="text-center mb-16">
              <div className="inline-flex items-center gap-2 px-5 py-2 bg-emerald-500/10 text-emerald-400 rounded-full text-sm font-bold uppercase tracking-widest mb-8 border border-emerald-500/20 shadow-[0_0_20px_rgba(16,185,129,0.1)]">
                <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 shadow-[0_0_10px_#10b981] animate-pulse" /> LIVE
              </div>
              <h3 className="text-4xl md:text-5xl font-black tracking-tight mb-6">{t('landing.live.title')}</h3>
              <p className="text-xl text-neutral-400 max-w-2xl mx-auto">{t('landing.live.desc')}</p>
            </motion.div>
            
            <motion.div {...fadeIn} transition={{ delay: 0.2 }} className="bg-black/50 backdrop-blur-xl rounded-[2.5rem] overflow-hidden border border-white/10 shadow-2xl">
              <LiveFeed standalone={true} />
            </motion.div>
          </div>
        </section>

        {/* Pricing */}
        <section id="pricing" className="px-6 py-32 max-w-6xl mx-auto relative">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-2xl h-96 bg-primary/10 blur-[120px] rounded-full pointer-events-none" />
          
          <motion.div {...fadeIn} className="text-center mb-20 relative z-10">
            <h3 className="text-4xl md:text-5xl font-black tracking-tight mb-6">{t('landing.pricing.title')}</h3>
            <p className="text-xl text-neutral-500 max-w-2xl mx-auto">{t('landing.pricing.desc')}</p>
          </motion.div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl mx-auto relative z-10">
            
            {/* Free */}
            <motion.div {...fadeIn} transition={{ delay: 0.1 }} className="bg-white dark:bg-[#0a0a0a] p-10 md:p-14 rounded-[2.5rem] border border-neutral-200 dark:border-neutral-800/60 shadow-sm flex flex-col hover:shadow-xl transition-shadow">
              <h4 className="text-3xl font-bold mb-3 text-neutral-900 dark:text-white">{t('landing.price.free')}</h4>
              <p className="text-lg text-neutral-500 mb-10">{t('landing.price.free.desc')}</p>
              <div className="text-6xl font-black mb-12 text-neutral-900 dark:text-white font-mono">$0<span className="text-2xl text-neutral-400 font-sans ml-2">{t('landing.price.month')}</span></div>
              
              <ul className="flex flex-col gap-5 mb-12 flex-1">
                <li className="flex items-center gap-4 text-lg font-medium text-neutral-700 dark:text-neutral-300"><Check size={24} className="text-emerald-500" /> {t('landing.plan.feat.basic')}</li>
                <li className="flex items-center gap-4 text-lg font-medium text-neutral-700 dark:text-neutral-300"><Check size={24} className="text-emerald-500" /> {t('landing.plan.feat.filters')}</li>
                <li className="flex items-center gap-4 text-lg font-medium text-neutral-700 dark:text-neutral-300"><Check size={24} className="text-emerald-500" /> {t('landing.plan.feat.warns')}</li>
              </ul>
              
              <a href="https://t.me/se1dhe_bot" className="w-full py-5 text-center rounded-2xl font-bold text-lg bg-neutral-100 dark:bg-neutral-800 text-neutral-900 dark:text-white hover:bg-neutral-200 dark:hover:bg-neutral-700 transition-colors">
                {t('landing.plan.cta.free')}
              </a>
            </motion.div>

            {/* Pro */}
            <motion.div {...fadeIn} transition={{ delay: 0.2 }} className="bg-gradient-to-b from-primary/5 to-transparent dark:from-primary/10 dark:to-transparent p-10 md:p-14 rounded-[2.5rem] border-2 border-primary relative flex flex-col shadow-[0_0_40px_rgba(220,38,38,0.1)]">
              <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-primary text-white px-6 py-2 rounded-full text-sm font-black uppercase tracking-widest shadow-lg shadow-primary/30">Most Popular</div>
              <h4 className="text-3xl font-bold mb-3 text-neutral-900 dark:text-white">{t('landing.price.pro')}</h4>
              <p className="text-lg text-neutral-500 mb-10">{t('landing.price.pro.desc')}</p>
              <div className="text-6xl font-black mb-12 text-primary font-mono">~ $5<span className="text-2xl text-neutral-400 font-sans ml-2">{t('landing.price.month')}</span></div>
              
              <ul className="flex flex-col gap-5 mb-12 flex-1">
                <li className="flex items-center gap-4 text-lg font-medium text-neutral-700 dark:text-neutral-300"><Check size={24} className="text-primary" /> {t('landing.plan.feat.ai')}</li>
                <li className="flex items-center gap-4 text-lg font-medium text-neutral-700 dark:text-neutral-300"><Check size={24} className="text-primary" /> {t('landing.plan.feat.raid')}</li>
                <li className="flex items-center gap-4 text-lg font-medium text-neutral-700 dark:text-neutral-300"><Check size={24} className="text-primary" /> {t('landing.plan.feat.priority')}</li>
              </ul>
              
              <a href="https://t.me/se1dhe_bot" className="w-full py-5 text-center rounded-2xl font-bold text-lg bg-gradient-to-r from-primary to-amber-500 hover:from-primary/90 hover:to-amber-500/90 text-white shadow-[0_8px_30px_-4px_rgba(220,38,38,0.4)] transition-transform active:scale-95">
                {t('landing.plan.cta.pro')}
              </a>
            </motion.div>

          </div>
        </section>

      </main>

      {/* Footer */}
      <footer className="border-t border-neutral-200 dark:border-neutral-800/60 py-16 px-6 bg-white dark:bg-[#0a0a0a]">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-primary text-white">
              <ShieldCheck size={18} />
            </div>
            <span className="font-bold text-lg text-neutral-900 dark:text-white">RedQueen</span>
          </div>
          <p className="text-neutral-500 font-medium">© 2026 RedQueen. {t('landing.footer.rights')}</p>
        </div>
      </footer>
    </div>
  );
}
