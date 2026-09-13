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
      const res = await api.triggers(chatId);
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
      await api.createTrigger(chatId, { trigger_word: word, reply_text: reply, is_regex: isRegex });
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
      await api.deleteTrigger(chatId, tid);
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
      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t("sec.triggers")}</div>
      <div className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-2xl p-4 mb-4 shadow-sm w-full" style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
        <div className="row-desc">{t("triggers.desc")}</div>
        
        {error && <div className="badge badge-danger">{error}</div>}

        <div style={{ marginTop: '0.5rem', fontWeight: 600, fontSize: '15px' }}>{t("triggers.add")}</div>
        
        <input className="w-full px-4 py-3 bg-neutral-50 dark:bg-neutral-950 border border-neutral-200 dark:border-neutral-800 rounded-xl focus:outline-none focus:border-primary/50 transition-colors font-medium text-[15px]" value={word} onChange={(e) => setWord(e.target.value)} placeholder={t("triggers.phrase.ph")} />
        <textarea className="w-full px-4 py-3 bg-neutral-50 dark:bg-neutral-950 border border-neutral-200 dark:border-neutral-800 rounded-xl focus:outline-none focus:border-primary/50 transition-colors font-medium text-[15px]" style={{ minHeight: '80px', resize: 'vertical' }} value={reply} onChange={(e) => setReply(e.target.value)} placeholder={t("triggers.reply.ph")}></textarea>
        
        <Row title={t("triggers.regex")}>
          <Toggle checked={isRegex} onChange={setIsRegex} />
        </Row>
        
        <button className="w-full flex items-center justify-center gap-2 py-3 bg-primary hover:bg-primary-dark text-white rounded-xl font-bold transition-all active:scale-95 shadow-md shadow-primary/20 text-[15px]" onClick={handleCreate} disabled={!word || !reply}>
          {t("triggers.btn.add")}
        </button>
      </div>

      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2" style={{ marginTop: '1.5rem' }}>{t("triggers.active")}</div>
      <div className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-2xl p-2 mb-4 shadow-sm w-full">
        {triggers.length === 0 ? (
          <div className="card-pad row-desc">{t("triggers.empty")}</div>
        ) : (
          triggers.map(trig => (
            <div key={trig.id} className="card-pad" style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ fontFamily: 'monospace', color: 'var(--tg-theme-accent-color)', fontWeight: 600 }}>
                  {trig.trigger_word}
                  {trig.is_regex && <span className="badge badge-gold" style={{ marginLeft: '6px' }}>{t("triggers.regexBadge")}</span>}
                </div>
                <button className="w-full flex items-center justify-center gap-2 py-3 bg-red-500 hover:bg-red-600 text-white rounded-xl font-bold transition-all active:scale-95 shadow-md shadow-red-500/20 text-[15px]" style={{ padding: '4px 10px', fontSize: '13px' }} onClick={() => handleDelete(trig.id)}>
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
