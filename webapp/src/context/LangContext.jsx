import { createContext, useContext, useMemo, useState } from 'react'
import { LOCALES, resolveLang } from '../i18n/translations'
import { tgLang } from '../lib/telegram'

const LangContext = createContext(null)

export function LangProvider({ children }) {
  const [lang, setLang] = useState(() => {
    const saved = localStorage.getItem('rq_lang')
    return resolveLang(saved || tgLang())
  })

  const value = useMemo(() => {
    const dict = LOCALES[lang]
    const t = (key, vars) => {
      let s = dict[key] ?? key
      if (vars) for (const [k, v] of Object.entries(vars)) s = s.replaceAll(`{${k}}`, v)
      return s
    }
    const setLangPersist = (l) => {
      const r = resolveLang(l)
      localStorage.setItem('rq_lang', r)
      setLang(r)
    }
    return { lang, setLang: setLangPersist, t }
  }, [lang])

  return <LangContext.Provider value={value}>{children}</LangContext.Provider>
}

export const useLang = () => useContext(LangContext)
