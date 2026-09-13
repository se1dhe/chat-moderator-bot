import React, { useState, useEffect } from 'react';
import { Toggle } from '../components/ui';
import { api } from '../lib/api';

export default function Triggers({ chatId, t }) {
  const [triggers, setTriggers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [word, setWord] = useState('');
  const [reply, setReply] = useState('');
  const [isRegex, setIsRegex] = useState(false);
  const [error, setError] = useState(null);

  const fetchTriggers = async () => {
    try {
      const res = await api.get(`/chats/${chatId}/triggers`);
      setTriggers(res);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTriggers();
  }, [chatId]);

  const handleCreate = async () => {
    if (!word || !reply) return;
    try {
      await api.post(`/chats/${chatId}/triggers`, { trigger_word: word, reply_text: reply, is_regex: isRegex });
      setWord('');
      setReply('');
      fetchTriggers();
    } catch (e) {
      if (window.Telegram?.WebApp) {
        window.Telegram.WebApp.showAlert(e.message);
      } else {
        alert(e.message);
      }
    }
  };

  const handleDelete = async (tid) => {
    try {
      await api.del(`/chats/${chatId}/triggers/${tid}`);
      fetchTriggers();
    } catch (e) {
      if (window.Telegram?.WebApp) {
        window.Telegram.WebApp.showAlert(e.message);
      } else {
        alert(e.message);
      }
    }
  };

  if (loading) return <div className="p-4 text-center text-text-muted">Loading triggers...</div>;

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h2 className="text-xl font-display font-bold">{t ? t("sec.triggers") : "Auto-Replies"}</h2>
        <p className="text-sm text-[var(--tg-theme-hint-color)]">Configure the bot to reply automatically to specific phrases or commands.</p>
      </div>
      
      {error && <div className="text-red-500 text-sm">{error}</div>}

      <div className="card" style={{ padding: '16px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <h3 className="font-bold text-sm">Add New Trigger</h3>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <div className="text-sm font-medium">Phrase or Command</div>
          <input className="input" style={{ width: '100%' }} value={word} onChange={(e) => setWord(e.target.value)} placeholder="e.g. /rules or price" />
        </div>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <div className="text-sm font-medium">Reply Text</div>
          <textarea className="input" style={{ width: '100%', minHeight: '80px', fontFamily: 'inherit' }} value={reply} onChange={(e) => setReply(e.target.value)} placeholder="The bot will send this..."></textarea>
        </div>
        
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span className="text-sm">Use Regex</span>
          <Toggle checked={isRegex} onChange={setIsRegex} />
        </div>
        
        <button className="btn btn-primary" style={{ width: '100%', padding: '12px' }} onClick={handleCreate} disabled={!word || !reply}>
          Add Trigger
        </button>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        <h3 className="font-bold text-sm">Active Triggers</h3>
        {triggers.length === 0 ? (
          <div className="text-sm text-[var(--tg-theme-hint-color)]">No triggers found.</div>
        ) : (
          triggers.map(trig => (
            <div key={trig.id} className="card" style={{ padding: '12px', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '16px' }}>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: '14px', color: 'var(--tg-theme-accent-color)', fontFamily: 'monospace' }}>
                  {trig.trigger_word} {trig.is_regex && <span style={{ fontSize: '10px', background: 'rgba(255,255,255,0.1)', padding: '2px 4px', borderRadius: '4px', marginLeft: '6px' }}>REGEX</span>}
                </div>
                <div style={{ fontSize: '14px', color: 'var(--tg-theme-text-color)', marginTop: '4px' }}>{trig.reply_text}</div>
              </div>
              <button className="btn btn-danger" style={{ fontSize: "12px", padding: "6px 12px", borderRadius: "8px" }} onClick={() => handleDelete(trig.id)}>Delete</button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
