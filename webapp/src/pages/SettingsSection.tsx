import { useParams } from 'react-router-dom';
import { useLang } from '../context/LangContext';
import { useChatSettings } from '../context/ChatSettingsContext';
import { Spinner } from '../components/ui';

import Triggers from './Triggers';
import Captcha from './settings/Captcha';
import Antiflood from './settings/Antiflood';
import Filters from './settings/Filters';
import Modes from './settings/Modes';
import AI from './settings/AI';
import Raid from './settings/Raid';
import Warns from './settings/Warns';
import Exempt from './settings/Exempt';
import AutoComment from './settings/AutoComment';
import Welcome from './settings/Welcome';
import Webhooks from './settings/Webhooks';
import RBAC from './settings/RBAC';

export function SettingsSection() {
  const { section } = useParams<{ section: string }>();
  const { t } = useLang();
  const s = useChatSettings();
  
  if (!s.draft) return <div className="flex-1 flex items-center justify-center py-12"><Spinner /></div>;

  const map: Record<string, JSX.Element> = {
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
  };
  
  const el = section && map[section];
  
  return <div className="w-full animate-in fade-in slide-in-from-right-4 duration-300">{el ?? null}</div>;
}
