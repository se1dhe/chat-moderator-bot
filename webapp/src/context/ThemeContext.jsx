import { createContext, useContext, useEffect, useState } from 'react'
import { isTelegram } from '../lib/telegram'

const ThemeContext = createContext()
const tg = window.Telegram?.WebApp

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('theme') || (tg?.colorScheme === 'light' ? 'light' : 'dark')
  })

  useEffect(() => {
    const root = document.documentElement
    if (theme === 'light') {
      root.classList.add('light')
      root.classList.remove('dark')
      try {
        tg?.setHeaderColor?.('#FAFAFA')
        tg?.setBackgroundColor?.('#FAFAFA')
      } catch {}
    } else {
      root.classList.add('dark')
      root.classList.remove('light')
      try {
        tg?.setHeaderColor?.('#09090B')
        tg?.setBackgroundColor?.('#09090B')
      } catch {}
    }
    localStorage.setItem('theme', theme)
  }, [theme])

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark')
  }

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  return useContext(ThemeContext)
}
