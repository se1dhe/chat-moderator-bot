import React, { useState, useEffect } from 'react';
import { api } from '../../lib/api';
import { useLang } from '../../context/LangContext';
import { Row, SectionLabel, Spinner } from '../../components/ui';
import { Trash2, Shield, UserPlus, ShieldAlert } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

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
      const data = await api.get(`/chats/${chatId}/moderators`);
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
      await api.post(`/chats/${chatId}/moderators`, {
        username: usernameInput.trim().replace('@', '')
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
      await api.del(`/chats/${chatId}/moderators/${uid}`);
      fetchMods();
    } catch (e) {
      console.error(e);
      setError(t('rbac_remove_error') || 'Error removing moderator');
    }
  };

  if (loading) {
    return (
      <div className="p-12 flex justify-center items-center">
        <Spinner />
      </div>
    );
  }

  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60 rounded-2xl p-4 mb-4 shadow-sm w-full space-y-4">
        
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-primary/10 dark:bg-primary/20 flex items-center justify-center shrink-0">
            <ShieldAlert size={20} className="text-primary" />
          </div>
          <div>
            <h3 className="font-bold text-[15px] dark:drop-shadow-[0_2px_10px_rgba(0,0,0,1)] text-neutral-900 dark:text-neutral-50">{t('rbac.title') || 'Добавить модератора'}</h3>
            <p className="text-[12px] text-neutral-500 leading-tight mt-0.5">
              Модераторы могут изменять настройки бота для этой группы.
            </p>
          </div>
        </div>

        <div className="flex gap-2 relative">
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
            <span className="text-neutral-400 font-medium">@</span>
          </div>
          <input 
            className="w-full pl-8 pr-4 py-3 bg-neutral-50 dark:bg-black border border-neutral-200 dark:border-neutral-800/60 rounded-xl focus:outline-none focus:border-primary/50 transition-colors font-medium text-[15px] shadow-inner"
            placeholder={t('rbac_username_placeholder') || 'username'}
            value={usernameInput}
            onChange={(e) => setUsernameInput(e.target.value)}
            disabled={adding}
            onKeyDown={(e) => e.key === 'Enter' && handleAdd()}
          />
          <button 
            className="shrink-0 px-5 flex items-center justify-center gap-2 bg-gradient-to-r from-red-600 to-red-500 hover:from-red-500 hover:to-red-400 text-white rounded-xl font-bold transition-all active:scale-95 shadow-[0_4px_20px_-4px_rgba(220,38,38,0.5)] disabled:opacity-50 disabled:shadow-none disabled:active:scale-100"
            onClick={handleAdd}
            disabled={adding || !usernameInput.trim()}
          >
            {adding ? <Spinner /> : <UserPlus size={18} className="drop-shadow-md" />}
          </button>
        </div>
        {error && (
          <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} className="text-red-500 text-[13px] font-medium bg-red-500/10 p-2.5 rounded-lg border border-red-500/20">
            {error}
          </motion.div>
        )}
      </div>

      <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60 rounded-2xl p-2 mb-4 shadow-sm w-full">
        <SectionLabel>{t('rbac_moderators_list') || 'МОДЕРАТОРЫ'}</SectionLabel>
        {mods.length === 0 ? (
          <div className="p-8 text-center flex flex-col items-center justify-center gap-2 text-neutral-400 dark:text-neutral-500">
            <Shield size={32} className="opacity-20" />
            <span className="text-sm">{t('rbac_no_moderators') || 'Модераторы не найдены.'}</span>
          </div>
        ) : (
          <div className="flex flex-col">
            <AnimatePresence>
              {mods.map(mod => (
                <motion.div
                  key={mod.user_id}
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.95, height: 0 }}
                  className="flex items-center justify-between p-3 border-b border-neutral-100 dark:border-neutral-800/50 last:border-0"
                >
                  <div className="flex items-center gap-3 overflow-hidden">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shrink-0 shadow-lg shadow-blue-500/20 text-white font-bold">
                      {(mod.full_name || mod.username || String(mod.user_id))[0].toUpperCase()}
                    </div>
                    <div className="flex flex-col overflow-hidden">
                      <span className="font-bold text-[14px] text-neutral-900 dark:text-neutral-50 truncate dark:drop-shadow-[0_1px_5px_rgba(0,0,0,1)]">
                        {mod.full_name || `@${mod.username}`}
                      </span>
                      <span className="text-[12px] text-neutral-500 font-mono truncate">
                        {mod.user_id}
                      </span>
                    </div>
                  </div>
                  <button 
                    className="p-2 text-red-400 hover:text-red-500 hover:bg-red-500/10 rounded-lg transition-colors shrink-0"
                    onClick={() => handleRemove(mod.user_id)}
                  >
                    <Trash2 size={18} />
                  </button>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        )}
      </div>
    </motion.div>
  );
}
