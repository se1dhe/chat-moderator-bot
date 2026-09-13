import { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { haptic } from '../lib/telegram';

export function TelegramBackButton() {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const tg = window.Telegram?.WebApp;
    if (!tg) return;

    if (location.pathname !== '/') {
      tg.BackButton.show();
    } else {
      tg.BackButton.hide();
    }

    const handleBack = () => {
      haptic('light');
      const parts = location.pathname.split('/').filter(Boolean);
      if (parts.length === 2 || (parts.length === 3 && ['members', 'quarantine', 'audit', 'stats'].includes(parts[2]))) {
        navigate('/');
      } else {
        navigate(-1);
      }
    };

    tg.BackButton.onClick(handleBack);

    return () => {
      tg.BackButton.offClick(handleBack);
      tg.BackButton.hide();
    };
  }, [location.pathname, navigate]);

  return null;
}
