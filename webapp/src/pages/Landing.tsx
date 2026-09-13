import { useState, useEffect } from 'react';
import { ShieldCheck, Zap, Activity, Check, Menu, X, ArrowRight } from 'lucide-react';
import { useLang } from '../context/LangContext';
import { api } from '../lib/api';
import { LiveFeed } from '../components/LiveFeed';
import { ThemeToggle } from '../components/ThemeToggle';

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
    <div className="min-h-screen bg-neutral-50 dark:bg-black text-neutral-900 dark:text-neutral-50 font-sans selection:bg-primary/20">
      
      {/* Header */}
      <header className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${scrolled ? 'bg-white/80 dark:bg-black/70 backdrop-blur-xl shadow-sm border-b border-neutral-200 dark:border-neutral-800/60/60/60/60 py-3' : 'bg-transparent py-5'}`}>
        <div className="max-w-7xl mx-auto px-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl overflow-hidden shadow-sm border border-neutral-200 dark:border-neutral-800/60/60/60/60">
              <img src="/app/logo.jpg" alt="Logo" className="w-full h-full object-cover" />
            </div>
            <span className="text-xl font-black tracking-tight">RedQueen</span>
          </div>

          <nav className="hidden md:flex items-center gap-8">
            {navLinks.map((link) => (
              <a key={link.href} href={link.href} className="text-sm font-semibold text-neutral-500 hover:text-neutral-900 dark:hover:text-neutral-50 transition-colors">
                {link.label}
              </a>
            ))}
            <div className="h-6 w-px bg-neutral-300 dark:bg-neutral-700" />
            <ThemeToggle />
            <a href="https://t.me/se1dhe_bot" className="px-5 py-2.5 bg-neutral-900 dark:bg-white text-white dark:text-neutral-900 rounded-xl font-bold hover:bg-neutral-800 dark:hover:bg-neutral-200 transition-colors">
              {t('landing.nav.login')}
            </a>
          </nav>

          <div className="md:hidden flex items-center gap-4">
            <ThemeToggle />
            <button className="text-neutral-900 dark:text-neutral-50" onClick={() => setMobileMenu(!mobileMenu)}>
              {mobileMenu ? <X size={28} /> : <Menu size={28} />}
            </button>
          </div>
        </div>
      </header>

      {/* Mobile Menu */}
      {mobileMenu && (
        <div className="fixed inset-0 z-40 bg-white dark:bg-neutral-950 pt-24 px-6 flex flex-col md:hidden animate-in slide-in-from-top-4">
          <nav className="flex flex-col gap-6">
            {navLinks.map((link) => (
              <a 
                key={link.href} 
                href={link.href} 
                className="text-2xl font-bold text-neutral-900 dark:text-neutral-50"
                onClick={() => setMobileMenu(false)}
              >
                {link.label}
              </a>
            ))}
          </nav>
          <a href="https://t.me/se1dhe_bot" className="mt-8 px-6 py-4 bg-primary text-white text-center rounded-2xl font-bold text-lg shadow-lg shadow-primary/20">
            {t('landing.nav.login')}
          </a>
        </div>
      )}

      <main className="pt-32">
        {/* Hero */}
        <section className="px-6 pb-24 md:pb-32 md:pt-16 max-w-7xl mx-auto text-center flex flex-col items-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary border border-primary/20 text-xs md:text-sm font-bold uppercase tracking-wider mb-8 animate-in slide-in-from-bottom-4">
            <ShieldCheck size={16} />
            {t('landing.hero.badge')}
          </div>
          
          <h1 className="text-5xl md:text-7xl font-black tracking-tight leading-[1.1] mb-6 max-w-4xl animate-in slide-in-from-bottom-5">
            {t('landing.hero.title1')}
            <span className="text-primary">{t('landing.hero.title_safe')}</span>
            {t('landing.hero.title2')}
            <span className="text-emerald-500">{t('landing.hero.title_clean')}</span>
          </h1>
          
          <p className="text-lg md:text-xl text-neutral-500 dark:text-neutral-400 mb-10 max-w-2xl leading-relaxed animate-in slide-in-from-bottom-6">
            {t('landing.hero.desc')}
          </p>
          
          <div className="flex flex-col sm:flex-row items-center gap-4 animate-in slide-in-from-bottom-7 w-full sm:w-auto">
            <a href="https://t.me/se1dhe_bot" className="w-full sm:w-auto px-8 py-4 bg-gradient-to-r from-red-600 to-red-500 hover:from-red-500 hover:to-red-400 text-white shadow-[0_4px_20px_-4px_rgba(220,38,38,0.5)] rounded-2xl font-bold text-lg flex items-center justify-center gap-2 transition-all hover:scale-105 active:scale-95 shadow-xl shadow-primary/20">
              {t('landing.hero.cta')} <ArrowRight size={20} />
            </a>
            <a href="#live" className="w-full sm:w-auto px-8 py-4 bg-neutral-200 dark:bg-neutral-800 text-neutral-900 dark:text-white rounded-2xl font-bold text-lg hover:bg-neutral-300 dark:hover:bg-neutral-700 transition-colors text-center">
              {t('landing.hero.demo')}
            </a>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-12 mt-24 w-full max-w-4xl animate-in slide-in-from-bottom-8">
            <div className="flex flex-col items-center p-6 rounded-3xl bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60/60/60/60 shadow-sm">
              <div className="text-4xl md:text-5xl font-black text-neutral-900 dark:text-white mb-2 font-mono">
                {stats.protected_chats.toLocaleString()}
              </div>
              <div className="text-sm font-bold text-neutral-500 uppercase tracking-wider">{t('landing.stats.chats')}</div>
            </div>
            <div className="flex flex-col items-center p-6 rounded-3xl bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60/60/60/60 shadow-sm">
              <div className="text-4xl md:text-5xl font-black text-neutral-900 dark:text-white mb-2 font-mono">
                {(stats.total_actions / 1000).toFixed(1)}K
              </div>
              <div className="text-sm font-bold text-neutral-500 uppercase tracking-wider">{t('landing.stats.actions')}</div>
            </div>
            <div className="flex flex-col items-center p-6 rounded-3xl bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60/60/60/60 shadow-sm">
              <div className="text-4xl md:text-5xl font-black text-primary mb-2 font-mono">
                {stats.ai_decisions.toLocaleString()}
              </div>
              <div className="text-sm font-bold text-neutral-500 uppercase tracking-wider">{t('landing.stats.ai')}</div>
            </div>
          </div>
        </section>

        {/* Features */}
        <section id="features" className="px-6 py-24 bg-white dark:bg-[#0a0a0a] border-y border-neutral-200 dark:border-neutral-800/60/60/60/60">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <h3 className="text-4xl md:text-5xl font-black tracking-tight mb-4">{t('landing.features.title')}</h3>
              <p className="text-xl text-neutral-500 max-w-2xl mx-auto">{t('landing.features.desc')}</p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {[
                { icon: ShieldCheck, title: t('landing.feat1.title'), desc: t('landing.feat1.desc') },
                { icon: Zap, title: t('landing.feat2.title'), desc: t('landing.feat2.desc') },
                { icon: Activity, title: t('landing.feat3.title'), desc: t('landing.feat3.desc') },
                { icon: ShieldCheck, title: t('landing.feat4.title'), desc: t('landing.feat4.desc') }
              ].map((f, i) => (
                <div key={i} className="bg-neutral-50 dark:bg-black p-8 rounded-3xl border border-neutral-200 dark:border-neutral-800/60/60/60/60 hover:border-primary/30 transition-colors">
                  <div className="w-14 h-14 bg-primary/10 text-primary rounded-2xl flex items-center justify-center mb-6">
                    <f.icon size={28} />
                  </div>
                  <h4 className="text-xl font-bold mb-3 text-neutral-900 dark:text-white">{f.title}</h4>
                  <p className="text-neutral-500 leading-relaxed">{f.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Live Feed */}
        <section id="live" className="px-6 py-24 bg-primary/5 dark:bg-primary/5 border-b border-primary/10">
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-12">
              <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 rounded-full text-xs font-bold uppercase tracking-wider mb-6 border border-emerald-500/20">
                <div className="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_10px_#10b981] animate-pulse" /> LIVE
              </div>
              <h3 className="text-4xl md:text-5xl font-black tracking-tight mb-4">{t('landing.live.title')}</h3>
              <p className="text-lg md:text-xl text-neutral-500 max-w-2xl mx-auto">{t('landing.live.desc')}</p>
            </div>
            
            <div className="bg-white dark:bg-[#0a0a0a] rounded-3xl overflow-hidden border border-neutral-200 dark:border-neutral-800/60/60/60/60 shadow-2xl shadow-primary/5">
              <LiveFeed standalone={true} />
            </div>
          </div>
        </section>

        {/* Pricing */}
        <section id="pricing" className="px-6 py-24 max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h3 className="text-4xl md:text-5xl font-black tracking-tight mb-4">{t('landing.pricing.title')}</h3>
            <p className="text-xl text-neutral-500 max-w-2xl mx-auto">{t('landing.pricing.desc')}</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            
            {/* Free */}
            <div className="bg-white dark:bg-[#0a0a0a] p-8 md:p-12 rounded-[2rem] border border-neutral-200 dark:border-neutral-800/60/60/60/60 shadow-sm flex flex-col">
              <h4 className="text-2xl font-bold mb-2 text-neutral-900 dark:text-white">{t('landing.price.free')}</h4>
              <p className="text-neutral-500 mb-8">{t('landing.price.free.desc')}</p>
              <div className="text-6xl font-black mb-10 text-neutral-900 dark:text-white font-mono">$0<span className="text-xl text-neutral-400 font-sans ml-2">{t('landing.price.month')}</span></div>
              
              <ul className="flex flex-col gap-4 mb-10 flex-1">
                <li className="flex items-center gap-3 font-medium text-neutral-700 dark:text-neutral-300"><Check size={20} className="text-emerald-500" /> {t('landing.plan.feat.basic')}</li>
                <li className="flex items-center gap-3 font-medium text-neutral-700 dark:text-neutral-300"><Check size={20} className="text-emerald-500" /> {t('landing.plan.feat.filters')}</li>
                <li className="flex items-center gap-3 font-medium text-neutral-700 dark:text-neutral-300"><Check size={20} className="text-emerald-500" /> {t('landing.plan.feat.warns')}</li>
              </ul>
              
              <a href="https://t.me/se1dhe_bot" className="w-full py-4 text-center rounded-xl font-bold bg-neutral-100 dark:bg-neutral-800 text-neutral-900 dark:text-white hover:bg-neutral-200 dark:hover:bg-neutral-700 transition-colors">
                {t('landing.plan.cta.free')}
              </a>
            </div>

            {/* Pro */}
            <div className="bg-gradient-to-b from-primary/10 to-transparent p-8 md:p-12 rounded-[2rem] border-2 border-primary relative flex flex-col">
              <div className="absolute -top-3.5 left-1/2 -translate-x-1/2 bg-primary text-white px-4 py-1 rounded-full text-xs font-black uppercase tracking-widest shadow-lg">Most Popular</div>
              <h4 className="text-2xl font-bold mb-2 text-neutral-900 dark:text-white">{t('landing.price.pro')}</h4>
              <p className="text-neutral-500 mb-8">{t('landing.price.pro.desc')}</p>
              <div className="text-6xl font-black mb-10 text-primary font-mono">~ $5<span className="text-xl text-neutral-400 font-sans ml-2">{t('landing.price.month')}</span></div>
              
              <ul className="flex flex-col gap-4 mb-10 flex-1">
                <li className="flex items-center gap-3 font-medium text-neutral-700 dark:text-neutral-300"><Check size={20} className="text-primary" /> {t('landing.plan.feat.ai')}</li>
                <li className="flex items-center gap-3 font-medium text-neutral-700 dark:text-neutral-300"><Check size={20} className="text-primary" /> {t('landing.plan.feat.raid')}</li>
                <li className="flex items-center gap-3 font-medium text-neutral-700 dark:text-neutral-300"><Check size={20} className="text-primary" /> {t('landing.plan.feat.priority')}</li>
              </ul>
              
              <a href="https://t.me/se1dhe_bot" className="w-full py-4 text-center rounded-xl font-bold bg-gradient-to-r from-red-600 to-red-500 hover:from-red-500 hover:to-red-400 text-white shadow-[0_4px_20px_-4px_rgba(220,38,38,0.5)] shadow-lg shadow-primary/20 transition-transform active:scale-95">
                {t('landing.plan.cta.pro')}
              </a>
            </div>

          </div>
        </section>

      </main>

      {/* Footer */}
      <footer className="border-t border-neutral-200 dark:border-neutral-800/60/60/60/60 py-12 px-6 bg-white dark:bg-[#0a0a0a]">
        <div className="max-w-7xl mx-auto flex flex-col items-center gap-4">
          <div className="flex items-center gap-2">
            <img src="/app/logo.jpg" alt="Logo" className="w-6 h-6 rounded-md" />
            <span className="font-bold text-neutral-900 dark:text-white">RedQueen</span>
          </div>
          <p className="text-sm text-neutral-500 font-medium">© 2026 RedQueen. {t('landing.footer.rights')}</p>
        </div>
      </footer>
    </div>
  );
}
