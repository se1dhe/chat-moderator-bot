import React, { useState, useEffect } from 'react';
import { Card, Input, Button, Toggle } from '../components/ui';
import api from '../lib/api';

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
        <p className="text-sm text-text-muted">Configure the bot to reply automatically to specific phrases or commands.</p>
      </div>
      
      {error && <div className="text-red-500 text-sm">{error}</div>}

      <Card className="p-4 space-y-4">
        <h3 className="font-bold text-sm">Add New Trigger</h3>
        <Input 
          label="Phrase or Command" 
          value={word} 
          onChange={(e) => setWord(e.target.value)} 
          placeholder="e.g. /rules or price"
        />
        <Input 
          label="Reply Text" 
          value={reply} 
          onChange={(e) => setReply(e.target.value)} 
          placeholder="The bot will send this..."
          multiline
        />
        <div className="flex justify-between items-center">
          <span className="text-sm">Use Regex</span>
          <Toggle checked={isRegex} onChange={setIsRegex} />
        </div>
        <Button onClick={handleCreate} disabled={!word || !reply} className="w-full">
          Add Trigger
        </Button>
      </Card>

      <div className="space-y-3">
        <h3 className="font-bold text-sm">Active Triggers</h3>
        {triggers.length === 0 ? (
          <div className="text-sm text-text-muted">No triggers found.</div>
        ) : (
          triggers.map(t => (
            <Card key={t.id} className="p-3 flex justify-between items-start gap-4">
              <div className="flex-1">
                <div className="font-mono text-sm text-accent">{t.trigger_word} {t.is_regex && <span className="text-xs bg-bg-elevated px-1 rounded text-text-muted">REGEX</span>}</div>
                <div className="text-sm text-text-secondary mt-1">{t.reply_text}</div>
              </div>
              <Button variant="danger" size="sm" onClick={() => handleDelete(t.id)}>Delete</Button>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
