import { useState, useEffect, useRef } from 'react'
import { useParams } from 'react-router-dom'
import { Plus, Lock } from 'lucide-react'
import { useLang } from '../context/LangContext'
import { useChatSettings } from '../context/ChatSettingsContext'
import { Toggle, Row, Segmented, Stepper, Slider, Chips, Spinner } from '../components/ui'
import { haptic, showAlert } from '../lib/telegram'
import { api } from '../lib/api'
import Triggers from './Triggers'
import Captcha from './settings/Captcha'
import Antiflood from './settings/Antiflood'
import Filters from './settings/Filters'
import Modes from './settings/Modes'
import AI from './settings/AI'
import Raid from './settings/Raid'
import Warns from './settings/Warns'
import Exempt from './settings/Exempt'
import AutoComment from './settings/AutoComment'
import Welcome from './settings/Welcome'
import Webhooks from './settings/Webhooks'
import RBAC from './settings/RBAC'

export function SettingsSection() {
  const { section } = useParams()
  const { t } = useLang()
  const s = useChatSettings()
  if (!s.draft) return <div className="content"><Spinner /></div>

  const map = {
    captcha: <Captcha s={s} t={t} />,
    antiflood: <Antiflood s={s} t={t} />,
    filters: <Filters s={s} t={t} />,
    modes: <Modes s={s} t={t} />,
    ai: <AI s={s} t={t} />,
    raid: <Raid s={s} t={t} />,
    warns: <Warns s={s} t={t} />,
    exempt: <Exempt s={s} t={t} />,
    autocomment: <AutoComment s={s} t={t} />,
    triggers: <Triggers chatId={s.chatId} t={t} />,
    welcome: <Welcome s={s} t={t} />,
    webhooks: <Webhooks s={s} t={t} />,
    rbac: <RBAC chatId={s.chatId} />,
  }
  return <div className="content fade-in">{map[section] ?? null}</div>
}








// Penalty-duration steppers use minutes; 0 == permanent. Cap at 7 days for the UI.




