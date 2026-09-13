import { openTelegramLink, haptic } from '../lib/telegram';
import { useLang } from '../context/LangContext';
import { ShieldCheck, Megaphone, Plus } from 'lucide-react';

export function GlobalOnboarding({ botUsername }: { botUsername?: string }) {
  const { t } = useLang();

  const addGroup = () => {
    haptic('success');
    const url = `https://t.me/${botUsername || 'RedQueenSecurity_Bot'}?startgroup=true&admin=restrict_members+delete_messages+invite_users+pin_messages+manage_video_chats+promote_members+change_info`;
    openTelegramLink(url);
  };

  const addChannel = () => {
    haptic('success');
    const url = `https://t.me/${botUsername || 'RedQueenSecurity_Bot'}?startchannel=true&admin=restrict_members+delete_messages+invite_users+pin_messages+manage_video_chats+promote_members+change_info+post_messages+edit_messages`;
    openTelegramLink(url);
  };

  return (
    <div className="flex-1 flex flex-col items-center justify-center text-center animate-in fade-in slide-in-from-bottom-2 px-2 py-12">
      <div className="w-20 h-20 bg-emerald-500/10 rounded-full flex items-center justify-center mb-6 mt-4">
        <Plus size={40} className="text-emerald-500" />
      </div>
      <h2 className="text-2xl font-black tracking-tight text-neutral-900 dark:text-neutral-50 mb-3">{t('start.title')}</h2>
      <p className="text-[15px] leading-relaxed text-neutral-500 mb-10 max-w-[280px]">
        {t('start.desc')}
      </p>

      <div className="w-full flex flex-col gap-3">
        <button 
          className="w-full flex items-center justify-center gap-2 py-3.5 bg-gradient-to-r from-primary to-primary-light hover:from-primary-dark hover:to-primary text-white rounded-xl font-bold transition-all active:scale-95 shadow-lg shadow-primary/20" 
          onClick={addGroup}
        >
          <ShieldCheck size={20} />
          {t('start.btn.group')}
        </button>

        <button 
          className="w-full flex items-center justify-center gap-2 py-3.5 bg-neutral-200 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 rounded-xl font-bold transition-all active:scale-95 border border-neutral-300 dark:border-neutral-700" 
          onClick={addChannel}
        >
          <Megaphone size={20} />
          {t('start.btn.channel')}
        </button>
      </div>
    </div>
  );
}
