import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { ShieldCheck, Activity, Zap, Check, Menu, X, ArrowRight } from 'lucide-react';
import { LiveFeed } from '../components/LiveFeed';
import { useLang } from '../context/LangContext';
import { API_BASE } from '../lib/api';

export function Landing() {
  const { t, lang, setLang } = useLang();
  const [stats, setStats] = useState({ chats: 0, mod_actions: 0, ai_verdicts: 0 });
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const ctrl = new AbortController();
    fetch(`${API_BASE}/stats/global`, { signal: ctrl.signal })
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(err => {
        if (err.name !== 'AbortError') console.error(err);
      });
    return () => ctrl.abort();
  }, []);

  const cycle = { en: 'ru', ru: 'uk', uk: 'en' };

  return (
    <div className="landing-page" style={{ 
      minHeight: '100vh', 
      background: '#07070e', 
      color: '#fff',
      overflowX: 'hidden'
    }}>
      
      {/* Navbar */}
      <nav style={{ 
        position: 'fixed', top: 0, left: 0, right: 0, zIndex: 100, 
        background: 'rgba(7,7,14,0.85)', backdropFilter: 'blur(12px)',
        borderBottom: '1px solid rgba(255,255,255,0.05)',
        padding: '16px 24px'
      }}>
        <div style={{ maxWidth: 1200, margin: '0 auto', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <div style={{ width: 36, height: 36, borderRadius: '10px', overflow: 'hidden' }}>
              <img src="/app/logo.jpg" alt="Logo" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            </div>
            <h1 style={{ fontSize: 20, fontWeight: 800, letterSpacing: '-0.5px' }}>
              RED<span style={{ color: '#ef4444' }}>QUEEN</span>
            </h1>
          </div>
          
          <div className="desktop-nav" style={{ display: 'flex', alignItems: 'center', gap: 32 }}>
            <a href="#features" style={{ color: '#aaa', textDecoration: 'none', fontSize: 15, fontWeight: 500, transition: 'color 0.2s' }}>{t('landing.nav.features')}</a>
            <a href="#live" style={{ color: '#aaa', textDecoration: 'none', fontSize: 15, fontWeight: 500, transition: 'color 0.2s' }}>{t('landing.nav.live')}</a>
            <a href="#pricing" style={{ color: '#aaa', textDecoration: 'none', fontSize: 15, fontWeight: 500, transition: 'color 0.2s' }}>{t('landing.nav.pricing')}</a>
            
            <button onClick={() => setLang(cycle[lang])} style={{ background: 'rgba(255,255,255,0.1)', border: 'none', color: '#fff', padding: '6px 12px', borderRadius: 20, cursor: 'pointer', fontWeight: 600, fontSize: 13, textTransform: 'uppercase' }}>
              {lang}
            </button>
            <a href="https://t.me/se1dhe_bot" className="btn btn-primary" style={{ padding: '8px 20px', borderRadius: 100, textDecoration: 'none', fontWeight: 600, fontSize: 14 }}>
              {t('landing.nav.login')}
            </a>
          </div>
          
          <button className="mobile-menu-btn" onClick={() => setMenuOpen(!menuOpen)} style={{ display: 'none', background: 'none', border: 'none', color: '#fff' }}>
            {menuOpen ? <X /> : <Menu />}
          </button>
        </div>
      </nav>

      {/* Mobile Menu */}
      {menuOpen && (
        <div style={{ position: 'fixed', top: 69, left: 0, right: 0, bottom: 0, background: '#07070e', zIndex: 99, padding: 24, display: 'flex', flexDirection: 'column', gap: 24 }}>
           <a href="#features" onClick={() => setMenuOpen(false)} style={{ color: '#fff', fontSize: 24, textDecoration: 'none', fontWeight: 600 }}>{t('landing.nav.features')}</a>
           <a href="#live" onClick={() => setMenuOpen(false)} style={{ color: '#fff', fontSize: 24, textDecoration: 'none', fontWeight: 600 }}>{t('landing.nav.live')}</a>
           <a href="#pricing" onClick={() => setMenuOpen(false)} style={{ color: '#fff', fontSize: 24, textDecoration: 'none', fontWeight: 600 }}>{t('landing.nav.pricing')}</a>
           <button onClick={() => { setLang(cycle[lang]); setMenuOpen(false) }} style={{ alignSelf: 'flex-start', background: 'rgba(255,255,255,0.1)', border: 'none', color: '#fff', padding: '10px 20px', borderRadius: 20, cursor: 'pointer', fontWeight: 600, fontSize: 16, textTransform: 'uppercase' }}>
              Language: {lang}
           </button>
        </div>
      )}

      <main style={{ paddingTop: 100 }}>
        
        {/* Hero Section */}
        <section style={{ maxWidth: 1000, margin: '0 auto', padding: '80px 24px', textAlign: 'center' }}>
          <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6, ease: 'easeOut' }}>
            <div style={{ display: 'inline-block', padding: '6px 16px', background: 'rgba(239, 68, 68, 0.1)', color: '#ef4444', borderRadius: 100, fontSize: 13, fontWeight: 700, marginBottom: 24, border: '1px solid rgba(239,68,68,0.2)' }}>
              {t('landing.hero.badge')}
            </div>
            <h2 style={{ fontSize: 'clamp(44px, 8vw, 80px)', fontWeight: 800, lineHeight: 1.05, marginBottom: 32, letterSpacing: '-2px' }}>
              {t('landing.hero.title1')}<span style={{ color: '#ef4444' }}>{t('landing.hero.title_safe')}</span>{t('landing.hero.title2')}<span style={{ color: '#ef4444' }}>{t('landing.hero.title_clean')}</span>.
            </h2>
            <p style={{ fontSize: 'clamp(18px, 4vw, 22px)', color: '#9ca3af', marginBottom: 48, lineHeight: 1.6, maxWidth: 800, margin: '0 auto 48px' }}>
              {t('landing.hero.desc')}
            </p>
            <div style={{ display: 'flex', gap: 16, justifyContent: 'center', flexWrap: 'wrap' }}>
              <a href="https://t.me/se1dhe_bot?startgroup=true" className="btn btn-primary" style={{ padding: '16px 32px', fontSize: 16, borderRadius: 100, textDecoration: 'none', display: 'flex', alignItems: 'center', gap: 10, fontWeight: 600 }}>
                <Zap size={20} /> {t('landing.hero.cta')}
              </a>
              <a href="#live" className="btn btn-secondary" style={{ padding: '16px 32px', fontSize: 16, borderRadius: 100, textDecoration: 'none', display: 'flex', alignItems: 'center', gap: 10, fontWeight: 600, background: 'rgba(255,255,255,0.05)', color: '#fff' }}>
                <Activity size={20} /> {t('landing.hero.demo')}
              </a>
            </div>
          </motion.div>
        </section>

        {/* Global Stats */}
        <section style={{ borderTop: '1px solid rgba(255,255,255,0.05)', borderBottom: '1px solid rgba(255,255,255,0.05)', background: 'rgba(0,0,0,0.3)' }}>
          <div style={{ maxWidth: 1200, margin: '0 auto', padding: '60px 24px' }}>
            <p style={{ textAlign: 'center', color: '#6b7280', fontWeight: 600, textTransform: 'uppercase', letterSpacing: 1, marginBottom: 40 }}>{t('landing.stats.title')}</p>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 40, textAlign: 'center' }}>
              <div>
                <div style={{ fontSize: 48, fontWeight: 800, color: '#fff', marginBottom: 8 }}>{stats.chats.toLocaleString()}+</div>
                <div style={{ color: '#9ca3af', fontWeight: 500 }}>{t('landing.stats.chats')}</div>
              </div>
              <div>
                <div style={{ fontSize: 48, fontWeight: 800, color: '#fff', marginBottom: 8 }}>{stats.mod_actions.toLocaleString()}+</div>
                <div style={{ color: '#9ca3af', fontWeight: 500 }}>{t('landing.stats.actions')}</div>
              </div>
              <div>
                <div style={{ fontSize: 48, fontWeight: 800, color: '#ef4444', marginBottom: 8 }}>{stats.ai_verdicts.toLocaleString()}+</div>
                <div style={{ color: '#9ca3af', fontWeight: 500 }}>{t('landing.stats.ai')}</div>
              </div>
            </div>
          </div>
        </section>

        {/* Features */}
        <section id="features" style={{ padding: '120px 24px', maxWidth: 1200, margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: 80 }}>
            <h3 style={{ fontSize: 'clamp(32px, 5vw, 48px)', fontWeight: 800, marginBottom: 20 }}>{t('landing.features.title')}</h3>
            <p style={{ fontSize: 20, color: '#9ca3af', maxWidth: 600, margin: '0 auto' }}>{t('landing.features.desc')}</p>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 24 }}>
            {[
              { icon: ShieldCheck, title: t('landing.feat1.title'), desc: t('landing.feat1.desc') },
              { icon: Zap, title: t('landing.feat2.title'), desc: t('landing.feat2.desc') },
              { icon: Activity, title: t('landing.feat3.title'), desc: t('landing.feat3.desc') },
              { icon: ShieldCheck, title: t('landing.feat4.title'), desc: t('landing.feat4.desc') }
            ].map((f, i) => (
              <div key={i} style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.05)', padding: 40, borderRadius: 24, transition: 'transform 0.2s', cursor: 'default' }} className="feature-card">
                <div style={{ width: 56, height: 56, background: 'rgba(239, 68, 68, 0.1)', color: '#ef4444', borderRadius: 16, display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: 24 }}>
                  <f.icon size={28} />
                </div>
                <h4 style={{ fontSize: 24, fontWeight: 700, marginBottom: 16 }}>{f.title}</h4>
                <p style={{ color: '#9ca3af', lineHeight: 1.6 }}>{f.desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Live Feed */}
        <section id="live" style={{ padding: '120px 24px', background: 'rgba(239, 68, 68, 0.02)', borderTop: '1px solid rgba(255,255,255,0.05)', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
          <div style={{ maxWidth: 1000, margin: '0 auto' }}>
            <div style={{ textAlign: 'center', marginBottom: 60 }}>
              <div style={{ display: 'inline-flex', alignItems: 'center', gap: 8, padding: '6px 16px', background: 'rgba(34, 197, 94, 0.1)', color: '#22c55e', borderRadius: 100, fontSize: 13, fontWeight: 700, marginBottom: 24 }}>
                <div style={{ width: 8, height: 8, borderRadius: '50%', background: '#22c55e', boxShadow: '0 0 10px #22c55e' }} /> LIVE
              </div>
              <h3 style={{ fontSize: 'clamp(32px, 5vw, 48px)', fontWeight: 800, marginBottom: 20 }}>{t('landing.live.title')}</h3>
              <p style={{ fontSize: 20, color: '#9ca3af' }}>{t('landing.live.desc')}</p>
            </div>
            <div style={{ background: '#000', borderRadius: 24, overflow: 'hidden', border: '1px solid rgba(255,255,255,0.1)', boxShadow: '0 25px 50px -12px rgba(0,0,0,0.5)' }}>
              <LiveFeed standalone={true} />
            </div>
          </div>
        </section>

        {/* Pricing */}
        <section id="pricing" style={{ padding: '120px 24px', maxWidth: 1200, margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: 80 }}>
            <h3 style={{ fontSize: 'clamp(32px, 5vw, 48px)', fontWeight: 800, marginBottom: 20 }}>{t('landing.pricing.title')}</h3>
            <p style={{ fontSize: 20, color: '#9ca3af', maxWidth: 600, margin: '0 auto' }}>{t('landing.pricing.desc')}</p>
          </div>
          
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: 32, maxWidth: 900, margin: '0 auto' }}>
            
            {/* Free Tier */}
            <div style={{ background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.05)', padding: 48, borderRadius: 32, display: 'flex', flexDirection: 'column' }}>
              <h4 style={{ fontSize: 24, fontWeight: 700, marginBottom: 8 }}>{t('landing.price.free')}</h4>
              <p style={{ color: '#9ca3af', marginBottom: 32 }}>{t('landing.price.free.desc')}</p>
              <div style={{ fontSize: 56, fontWeight: 800, marginBottom: 40 }}>$0<span style={{ fontSize: 20, color: '#6b7280', fontWeight: 500 }}>{t('landing.price.month')}</span></div>
              
              <ul style={{ listStyle: 'none', padding: 0, margin: '0 0 40px', display: 'flex', flexDirection: 'column', gap: 16, flex: 1 }}>
                <li style={{ display: 'flex', alignItems: 'center', gap: 12 }}><Check size={20} color="#22c55e" /> {t('landing.plan.feat.basic')}</li>
                <li style={{ display: 'flex', alignItems: 'center', gap: 12 }}><Check size={20} color="#22c55e" /> {t('landing.plan.feat.filters')}</li>
                <li style={{ display: 'flex', alignItems: 'center', gap: 12 }}><Check size={20} color="#22c55e" /> {t('landing.plan.feat.warns')}</li>
              </ul>
              
              <a href="https://t.me/se1dhe_bot" className="btn btn-secondary" style={{ width: '100%', padding: '16px', borderRadius: 16, textAlign: 'center', fontWeight: 600, background: 'rgba(255,255,255,0.05)', color: '#fff', textDecoration: 'none' }}>
                {t('landing.plan.cta.free')}
              </a>
            </div>

            {/* Pro Tier */}
            <div style={{ background: 'linear-gradient(180deg, rgba(239, 68, 68, 0.1) 0%, rgba(0,0,0,0) 100%)', border: '1px solid rgba(239,68,68,0.3)', padding: 48, borderRadius: 32, display: 'flex', flexDirection: 'column', position: 'relative' }}>
              <div style={{ position: 'absolute', top: -14, left: '50%', transform: 'translateX(-50%)', background: '#ef4444', color: '#fff', padding: '4px 16px', borderRadius: 100, fontSize: 12, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 1 }}>Most Popular</div>
              <h4 style={{ fontSize: 24, fontWeight: 700, marginBottom: 8 }}>{t('landing.price.pro')}</h4>
              <p style={{ color: '#9ca3af', marginBottom: 32 }}>{t('landing.price.pro.desc')}</p>
              <div style={{ fontSize: 56, fontWeight: 800, marginBottom: 40, color: '#ef4444' }}>~ $5<span style={{ fontSize: 20, color: '#6b7280', fontWeight: 500 }}>{t('landing.price.month')}</span></div>
              
              <ul style={{ listStyle: 'none', padding: 0, margin: '0 0 40px', display: 'flex', flexDirection: 'column', gap: 16, flex: 1 }}>
                <li style={{ display: 'flex', alignItems: 'center', gap: 12 }}><Check size={20} color="#ef4444" /> {t('landing.plan.feat.ai')}</li>
                <li style={{ display: 'flex', alignItems: 'center', gap: 12 }}><Check size={20} color="#ef4444" /> {t('landing.plan.feat.raid')}</li>
                <li style={{ display: 'flex', alignItems: 'center', gap: 12 }}><Check size={20} color="#ef4444" /> {t('landing.plan.feat.priority')}</li>
              </ul>
              
              <a href="https://t.me/se1dhe_bot" className="btn btn-primary" style={{ width: '100%', padding: '16px', borderRadius: 16, textAlign: 'center', fontWeight: 600, textDecoration: 'none' }}>
                {t('landing.plan.cta.pro')}
              </a>
            </div>

          </div>
        </section>

      </main>

      <footer style={{ borderTop: '1px solid rgba(255,255,255,0.05)', padding: '40px 24px', textAlign: 'center', color: '#6b7280' }}>
        <div style={{ maxWidth: 1200, margin: '0 auto', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 16 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <img src="/app/logo.jpg" alt="Logo" style={{ width: 24, height: 24, borderRadius: 6 }} />
            <span style={{ fontWeight: 700, color: '#fff' }}>RedQueen</span>
          </div>
          <p>© 2026 RedQueen. {t('landing.footer.rights')}</p>
        </div>
      </footer>
    </div>
  );

