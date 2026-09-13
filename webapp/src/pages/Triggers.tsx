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
      <div className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-2xl p-4 mb-4 shadow-sm w-full flex flex-col gap-3">
        <div className="text-[13px] text-neutral-500 leading-snug">{t("triggers.desc")}</div>
        
        {error && <div className="px-2 py-0.5 bg-red-100 text-red-700 dark:bg-red-500/20 dark:text-red-400 rounded-md text-[11px] font-bold uppercase tracking-wider inline-flex items-center gap-1">{error}</div>}

        <div className="mt-2 font-semibold text-[15px]">{t("triggers.add")}</div>
        
        <input className="w-full px-4 py-3 bg-neutral-50 dark:bg-neutral-950 border border-neutral-200 dark:border-neutral-800 rounded-xl focus:outline-none focus:border-primary/50 transition-colors font-medium text-[15px]" value={word} onChange={(e) => setWord(e.target.value)} placeholder={t("triggers.phrase.ph")} />
        <textarea className="w-full px-4 py-3 bg-neutral-50 dark:bg-neutral-950 border border-neutral-200 dark:border-neutral-800 rounded-xl focus:outline-none focus:border-primary/50 transition-colors font-medium text-[15px] min-h-[80px] resize-y" value={reply} onChange={(e) => setReply(e.target.value)} placeholder={t("triggers.reply.ph")}></textarea>
        
        <Row title={t("triggers.regex")}>
          <Toggle checked={isRegex} onChange={setIsRegex} />
        </Row>
        
        <button className="w-full flex items-center justify-center gap-2 py-3 bg-primary hover:bg-primary-dark text-white rounded-xl font-bold transition-all active:scale-95 shadow-md shadow-primary/20 text-[15px]" onClick={handleCreate} disabled={!word || !reply}>
          {t("triggers.btn.add")}
        </button>
      </div>

      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2 mt-6">{t("triggers.active")}</div>
      <div className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-2xl p-2 mb-4 shadow-sm w-full">
        {triggers.length === 0 ? (
          <div className="p-4 text-[13px] text-neutral-500 leading-snug">{t("triggers.empty")}</div>
        ) : (
          triggers.map(trig => (
            <div key={trig.id} className="p-4 flex flex-col gap-2 border-b border-neutral-200 dark:border-neutral-800/50 last:border-0">
              <div className="flex justify-between items-center">
                <div className="font-mono text-primary font-semibold">
                  {trig.trigger_word}
                  {trig.is_regex && <span className="px-2 py-0.5 bg-amber-100 text-amber-700 dark:bg-amber-500/20 dark:text-amber-400 rounded-md text-[11px] font-bold uppercase tracking-wider ml-1.5">{t("triggers.regexBadge")}</span>}
                </div>
                <button className="w-full flex items-center justify-center gap-2 py-3 bg-red-500 hover:bg-red-600 text-white rounded-xl font-bold transition-all active:scale-95 shadow-md shadow-red-500/20 text-[15px] px-3 py-1 text-[13px]" onClick={() => handleDelete(trig.id)}>
                  {t("triggers.btn.delete")}
                </button>
              </div>
              <div className="text-sm text-neutral-700 dark:text-neutral-300">{trig.reply_text}</div>
            </div>
          ))
        )}
      </div>
    </>
  );
}
