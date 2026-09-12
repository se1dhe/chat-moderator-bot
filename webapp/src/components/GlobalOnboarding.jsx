import { useState } from 'react'
import { openTelegramLink, haptic } from '../lib/telegram'
import { useLang } from '../context/LangContext'
import { Rocket, ShieldCheck, Megaphone, Plus } from 'lucide-react'

export function GlobalOnboarding({ botUsername }) {
  const { t } = useLang()
  const [step, setStep] = useState(1)

  const next = () => {
    haptic('light')
    setStep((s) => s + 1)
  }

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

  const s1 = (
    <div className="center-state fade-in" style={{ padding: '0 20px', minHeight: '60vh', justifyContent: 'center' }}>
      <div className="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mb-6 mt-8 mx-auto">
        <Rocket size={32} className="text-red-500" />
      </div>
      <h2 className="text-2xl font-bold mb-4">{t('wn.title.1')}</h2>
      <p className="text-[var(--tg-theme-hint-color)] mb-8 leading-relaxed">
        {t('wn.desc.1')}
      </p>
      <button className="btn w-full" onClick={next}>{t('wn.btn.next')}</button>
    </div>
  )

  const s2 = (
    <div className="center-state fade-in" style={{ padding: '0 20px', minHeight: '60vh', justifyContent: 'center' }}>
      <div className="w-16 h-16 bg-yellow-500/20 rounded-full flex items-center justify-center mb-6 mt-8 mx-auto">
        <ShieldCheck size={32} className="text-yellow-500" />
      </div>
      <h2 className="text-xl font-bold mb-4">{t('wn.title.2')}</h2>
      <p className="text-[var(--tg-theme-hint-color)] mb-8 leading-relaxed">
        {t('wn.desc.2')}
      </p>
      
      <h2 className="text-xl font-bold mb-4">{t('wn.title.3')}</h2>
      <p className="text-[var(--tg-theme-hint-color)] mb-8 leading-relaxed">
        {t('wn.desc.3')}
      </p>

      <button className="btn w-full" onClick={next}>{t('wn.btn.next')}</button>
    </div>
  )

  const s3 = (
    <div className="center-state fade-in" style={{ padding: '0 20px', minHeight: '60vh', justifyContent: 'center' }}>
      <div className="w-16 h-16 bg-green-500/20 rounded-full flex items-center justify-center mb-6 mt-8 mx-auto">
        <Plus size={32} className="text-green-500" />
      </div>
      <h2 className="text-2xl font-bold mb-4">{t('start.title') || 'Добавление бота'}</h2>
      <p className="text-[var(--tg-theme-hint-color)] mb-8 leading-relaxed">
        {t('start.desc') || 'Выберите, куда добавить RedQueen, чтобы начать защиту. Бот автоматически настроится и появится в списке ваших чатов.'}
      </p>

      <button className="btn w-full flex items-center justify-center gap-2 mb-4" onClick={addGroup}>
        <ShieldCheck size={20} />
        {t('start.btn.group') || 'Добавить в Группу'}
      </button>

      <button className="btn-secondary w-full flex items-center justify-center gap-2" onClick={addChannel}>
        <Megaphone size={20} />
        {t('start.btn.channel') || 'Добавить в Канал'}
      </button>
    </div>
  )

  return (
    <div className="content" style={{ display: 'flex', flexDirection: 'column', minHeight: '100%' }}>
      {step === 1 && s1}
      {step === 2 && s2}
      {step === 3 && s3}
      
      <div className="flex justify-center gap-2 mt-auto pb-8">
        {[1, 2, 3].map((i) => (
          <div key={i} className={`w-2 h-2 rounded-full ${step === i ? 'bg-[var(--tg-theme-button-color)]' : 'bg-[var(--tg-theme-hint-color)] opacity-30'}`} />
        ))}
      </div>
    </div>
  )
}
