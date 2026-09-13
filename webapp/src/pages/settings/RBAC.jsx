import React, { useState, useEffect } from 'react';
import { api } from '../../lib/api';
import { useLang } from '../../context/LangContext';
import { Row, SectionLabel, Spinner } from '../../components/ui';
import { Trash2, Shield, UserPlus } from 'lucide-react';

export default function RBAC({ chatId }) {
  const { t } = useLang();
  const [mods, setMods] = useState([]);
  const [loading, setLoading] = useState(true);
  const [adding, setAdding] = useState(false);
  const [usernameInput, setUsernameInput] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchMods();
  }, [chatId]);

  const fetchMods = async () => {
    try {
      const data = await api.get(`/api/chats/${chatId}/moderators`);
      setMods(data);
    } catch (e) {
      console.error(e);
      setError(t('rbac_fetch_error') || 'Error fetching moderators');
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = async () => {
    if (!usernameInput.trim()) return;
    setAdding(true);
    setError(null);
    try {
      await api.post(`/api/chats/${chatId}/moderators`, {
        username: usernameInput.trim()
      });
      setUsernameInput('');
      fetchMods();
    } catch (e) {
      console.error(e);
      setError(e.response?.data?.reason || t('rbac_add_error') || 'Error adding moderator');
    } finally {
      setAdding(false);
    }
  };

  const handleRemove = async (uid) => {
    if (!confirm(t('rbac_remove_confirm') || 'Are you sure?')) return;
    try {
      await api.delete(`/api/chats/${chatId}/moderators/${uid}`);
      fetchMods();
    } catch (e) {
      console.error(e);
      setError(t('rbac_remove_error') || 'Error removing moderator');
    }
  };

  if (loading) {
    return (
      <div className="p-4 flex justify-center">
        <Spinner />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="card p-4 space-y-4">
        <div className="flex gap-2">
          <input 
            className="input flex-1"
            placeholder={t('rbac_username_placeholder') || '@username'}
            value={usernameInput}
            onChange={(e) => setUsernameInput(e.target.value)}
            disabled={adding}
          />
          <button 
            className="btn btn-primary"
            onClick={handleAdd}
            disabled={adding || !usernameInput.trim()}
          >
            {adding ? <Spinner size="sm" /> : <UserPlus size={18} />}
          </button>
        </div>
        {error && <div className="text-red-500 text-sm">{error}</div>}
      </div>

      <div className="card">
        <SectionLabel>{t('rbac_moderators_list') || 'Moderators'}</SectionLabel>
        {mods.length === 0 ? (
          <div className="p-4 text-center text-gray-500">
            {t('rbac_no_moderators') || 'No moderators found.'}
          </div>
        ) : (
          <div className="divide-y divide-white/5">
            {mods.map(mod => (
              <Row
                key={mod.user_id}
                title={mod.full_name || mod.username || String(mod.user_id)}
                subtitle={`@${mod.username || mod.user_id}`}
                icon={<Shield className="text-blue-500" />}
                right={
                  <button 
                    className="p-2 text-red-400 hover:text-red-300 transition-colors"
                    onClick={() => handleRemove(mod.user_id)}
                  >
                    <Trash2 size={18} />
                  </button>
                }
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
