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
    <div className="content" style={{ display: 'flex', flexDirection: 'column', minHeight: '100%' }}>
      <div className="center-state fade-in" style={{ padding: '0 20px', minHeight: '60vh', justifyContent: 'center' }}>
        <div style={{ width: 64, height: 64, background: 'rgba(34, 197, 94, 0.2)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '32px auto 24px' }}>
          <Plus size={32} color="#22c55e" />
        </div>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: 16 }}>{t('start.title') || 'Добавление бота'}</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: 32, lineHeight: 1.6 }}>
          {t('start.desc') || 'Выберите, куда добавить RedQueen, чтобы начать защиту. Бот автоматически настроится и появится в списке ваших чатов.'}
        </p>

        <button className="btn btn-primary btn-block" style={{ marginBottom: 16 }} onClick={addGroup}>
          <ShieldCheck size={20} />
          {t('start.btn.group') || 'Добавить в Группу'}
        </button>

        <button className="btn btn-block" onClick={addChannel}>
          <Megaphone size={20} />
          {t('start.btn.channel') || 'Добавить в Канал'}
        </button>
      </div>
    </div>
  )
}
