import { Moon, Sun } from 'lucide-react'
import { useTheme } from '../context/ThemeContext'
import { haptic } from '../lib/telegram'

export function ThemeToggle() {
  const { theme, toggleTheme } = useTheme()

  return (
    <button
      className="header-back"
      style={{ marginLeft: '4px' }}
      onClick={() => {
        haptic('light')
        toggleTheme()
      }}
      title="Toggle Theme"
    >
      {theme === 'dark' ? <Moon size={16} /> : <Sun size={16} />}
    </button>
  )
}
