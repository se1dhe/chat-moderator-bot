import { useState } from 'react'
import { openTelegramLink, haptic } from '../lib/telegram'
import { useLang } from '../context/LangContext'
import { Rocket, ShieldCheck, Megaphone, Plus } from 'lucide-react'

export function GlobalOnboarding({ botUsername }) {
  const { t } = useLang()

  const addGroup = () => {
    haptic('success')
    const url = `https://t.me/${botUsername || 'RedQueenSecurity_Bot'}?startgroup=true&admin=restrict_members+delete_messages+invite_users+pin_messages+manage_video_chats+promote_members+change_info`
    openTelegramLink(url)
  }

  const addChannel = () => {
    haptic('success')
    const url = `https://t.me/${botUsername || 'RedQueenSecurity_Bot'}?startchannel=true&admin=restrict_members+delete_messages+invite_users+pin_messages+manage_video_chats+promote_members+change_info+post_messages+edit_messages`
    openTelegramLink(url)
  }

  return (
    <div className="content flex flex-col min-h-full">
      <div className="center-state fade-in px-5 min-h-[60vh] justify-center">
        <div className="w-16 h-16 bg-green-500/20 rounded-full flex items-center justify-center mb-6 mt-8 mx-auto">
          <Plus size={32} className="text-green-500" />
        </div>
        <h2 className="text-2xl font-bold mb-4">{t('start.title')}</h2>
        <p className="text-tg-hint mb-8 leading-relaxed">
          {t('start.desc')}
        </p>

        <button className="btn w-full flex items-center justify-center gap-2 mb-4 bg-gradient-to-r from-red-500 to-red-600 text-white border-0 shadow-lg shadow-red-500/20" onClick={addGroup}>
          <ShieldCheck size={20} />
          {t('start.btn.group')}
        </button>

        <button className="btn w-full flex items-center justify-center gap-2 bg-tg-secondary border border-[var(--border)] text-tg-text" onClick={addChannel}>
          <Megaphone size={20} />
          {t('start.btn.channel')}
        </button>
      </div>
    </div>
  )
}
