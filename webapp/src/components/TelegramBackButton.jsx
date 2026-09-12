import { useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { haptic } from '../lib/telegram'

export function TelegramBackButton() {
  const navigate = useNavigate()
  const location = useLocation()

  useEffect(() => {
    const tg = window.Telegram?.WebApp
    if (!tg) return

    // Show back button if we are not on the root ChatPicker page
    if (location.pathname !== '/') {
      tg.BackButton.show()
    } else {
      tg.BackButton.hide()
    }

    const handleBack = () => {
      haptic('light')
      // If we are at the dashboard or any of the main tabs, go back to chat list
      const parts = location.pathname.split('/').filter(Boolean)
      if (parts.length === 2 || (parts.length === 3 && ['members', 'quarantine', 'audit', 'stats'].includes(parts[2]))) {
        navigate('/')
      } else {
        // Otherwise go back in history (e.g. out of a settings section)
        navigate(-1)
      }
    }

    tg.BackButton.onClick(handleBack)

    return () => {
      tg.BackButton.offClick(handleBack)
      tg.BackButton.hide()
    }
  }, [location.pathname, navigate])

  return null
}
