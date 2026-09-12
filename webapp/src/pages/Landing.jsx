import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Bot, ShieldCheck, Activity, Zap } from 'lucide-react';
import { LiveFeed } from '../components/LiveFeed';

export function Landing() {
  const [stats, setStats] = useState({ chats: 0, mod_actions: 0, ai_verdicts: 0 });

  useEffect(() => {
    fetch('/api/stats/global')
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(console.error);
  }, []);

  return (
    <div style={{ minHeight: '100vh', background: 'var(--tg-theme-bg-color, #0f0f0f)', color: 'var(--tg-theme-text-color, #ffffff)', padding: '0', display: 'flex', flexDirection: 'column' }}>
      
      {/* Navbar */}
      <header style={{ padding: '20px 24px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{ width: '32px', height: '32px', background: 'linear-gradient(135deg, #ef4444 0%, #7f1d1d 100%)', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Bot size={20} color="white" />
          </div>
          <h1 style={{ fontSize: '18px', fontWeight: 700, letterSpacing: '-0.5px' }}>RED<span style={{ color: '#ef4444' }}>QUEEN</span></h1>
        </div>
        <a href="https://t.me/ChatModeratorBot" className="btn btn-primary" style={{ padding: '8px 16px', fontSize: '14px', borderRadius: '20px', textDecoration: 'none' }}>
          Get Started
        </a>
      </header>

      <main style={{ flex: 1, maxWidth: '1200px', margin: '0 auto', width: '100%', padding: '40px 24px', display: 'flex', flexDirection: 'column', gap: '60px' }}>
        
        {/* Hero */}
        <section style={{ textAlign: 'center', maxWidth: '800px', margin: '0 auto', paddingTop: '40px' }}>
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
            <div style={{ display: 'inline-block', padding: '6px 16px', background: 'rgba(239, 68, 68, 0.1)', color: '#ef4444', borderRadius: '20px', fontSize: '13px', fontWeight: 600, marginBottom: '20px' }}>
              Next-Gen Autonomous AI Moderation
            </div>
            <h2 style={{ fontSize: 'clamp(40px, 8vw, 64px)', fontWeight: 800, lineHeight: 1.1, marginBottom: '24px', letterSpacing: '-1px' }}>
              Keep your communities <span style={{ color: '#ef4444' }}>safe</span> and <span style={{ color: '#ef4444' }}>clean</span>.
            </h2>
            <p style={{ fontSize: '18px', color: 'var(--tg-theme-hint-color, #888)', marginBottom: '40px', lineHeight: 1.6 }}>
              RedQueen is an advanced AI moderator that analyzes context, detects toxicity, bans scammers, and protects your Telegram groups 24/7.
            </p>
            <div style={{ display: 'flex', gap: '16px', justifyContent: 'center', flexWrap: 'wrap' }}>
              <a href="https://t.me/ChatModeratorBot" className="btn btn-primary" style={{ padding: '14px 28px', fontSize: '16px', borderRadius: '12px', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Zap size={18} /> Add to Telegram
              </a>
            </div>
          </motion.div>
        </section>

        {/* Live Feed & Stats */}
        <section style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px', alignItems: 'start' }}>
          
          <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.5, delay: 0.2 }}>
            <h3 style={{ fontSize: '20px', fontWeight: 700, marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Activity size={20} color="#ef4444" /> Live Action
            </h3>
            <LiveFeed />
          </motion.div>

          <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.5, delay: 0.3 }} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <h3 style={{ fontSize: '20px', fontWeight: 700, marginBottom: '0', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <ShieldCheck size={20} color="#ef4444" /> Global Impact
            </h3>
            
            <div className="card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '4px' }}>
              <div style={{ fontSize: '14px', color: 'var(--tg-theme-hint-color, #888)', fontWeight: 600, textTransform: 'uppercase' }}>Protected Communities</div>
              <div style={{ fontSize: '36px', fontWeight: 800, color: '#ef4444' }}>{stats.chats.toLocaleString()}</div>
            </div>
            
            <div className="card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '4px' }}>
              <div style={{ fontSize: '14px', color: 'var(--tg-theme-hint-color, #888)', fontWeight: 600, textTransform: 'uppercase' }}>Actions Taken</div>
              <div style={{ fontSize: '36px', fontWeight: 800, color: '#ef4444' }}>{stats.mod_actions.toLocaleString()}</div>
            </div>

            <div className="card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '4px' }}>
              <div style={{ fontSize: '14px', color: 'var(--tg-theme-hint-color, #888)', fontWeight: 600, textTransform: 'uppercase' }}>AI Verdicts</div>
              <div style={{ fontSize: '36px', fontWeight: 800, color: '#ef4444' }}>{stats.ai_verdicts.toLocaleString()}</div>
            </div>
          </motion.div>

        </section>

      </main>

      <footer style={{ padding: '40px 24px', textAlign: 'center', borderTop: '1px solid rgba(255,255,255,0.05)', color: 'var(--tg-theme-hint-color, #888)', fontSize: '14px' }}>
        &copy; {new Date().getFullYear()} RedQueen by Telonyx. All rights reserved.
      </footer>
    </div>
  );
}
