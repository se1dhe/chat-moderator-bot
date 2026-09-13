import React, { useState, useEffect } from 'react';
import { Toggle, Row, Spinner } from '../components/ui';
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

  if (loading) return <div className="content fade-in"><Spinner /></div>;

  return (
    <>
      <div className="section-label">{t("sec.triggers")}</div>
      <div className="card card-pad" style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
        <div className="row-desc">{t("triggers.desc")}</div>
        
        {error && <div className="badge badge-danger">{error}</div>}

        <div style={{ marginTop: '0.5rem', fontWeight: 600, fontSize: '15px' }}>{t("triggers.add")}</div>
        
        <input className="input" value={word} onChange={(e) => setWord(e.target.value)} placeholder={t("triggers.phrase.ph")} />
        <textarea className="input" style={{ minHeight: '80px', resize: 'vertical' }} value={reply} onChange={(e) => setReply(e.target.value)} placeholder={t("triggers.reply.ph")}></textarea>
        
        <Row title={t("triggers.regex")}>
          <Toggle checked={isRegex} onChange={setIsRegex} />
        </Row>
        
        <button className="btn btn-primary" onClick={handleCreate} disabled={!word || !reply}>
          {t("triggers.btn.add")}
        </button>
      </div>

      <div className="section-label" style={{ marginTop: '1.5rem' }}>{t("triggers.active")}</div>
      <div className="card">
        {triggers.length === 0 ? (
          <div className="card-pad row-desc">{t("triggers.empty")}</div>
        ) : (
          triggers.map(trig => (
            <div key={trig.id} className="card-pad" style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ fontFamily: 'monospace', color: 'var(--tg-theme-accent-color)', fontWeight: 600 }}>
                  {trig.trigger_word}
                  {trig.is_regex && <span className="badge badge-gold" style={{ marginLeft: '6px' }}>REGEX</span>}
                </div>
                <button className="btn btn-danger" style={{ padding: '4px 10px', fontSize: '13px' }} onClick={() => handleDelete(trig.id)}>
                  {t("triggers.btn.delete")}
                </button>
              </div>
              <div style={{ fontSize: '14px', color: 'var(--tg-theme-text-color)' }}>{trig.reply_text}</div>
            </div>
          ))
        )}
      </div>
    </>
  );
}
