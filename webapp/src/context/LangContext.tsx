import { createContext, useContext, useMemo, useState, ReactNode } from 'react';
import { LOCALES, resolveLang, Locales } from '../i18n/translations';
import { tgLang } from '../lib/telegram';
import { api } from '../lib/api';

interface LangContextType {
  lang: Locales;
  setLang: (l: string) => void;
  t: (key: string, vars?: Record<string, string | number>) => string;
}

const LangContext = createContext<LangContextType | null>(null);

export function LangProvider({ children }: { children: ReactNode }) {
  const [lang, setLang] = useState<Locales>(() => {
    const saved = localStorage.getItem('rq_lang');
    return resolveLang(saved || tgLang());
  });

  const value = useMemo(() => {
    const dict = LOCALES[lang];
    const t = (key: string, vars?: Record<string, string | number>) => {
      let s = dict[key] ?? key;
      if (vars) {
        for (const [k, v] of Object.entries(vars)) {
          s = s.replaceAll(`{${k}}`, String(v));
        }
      }
      return s;
    };
    const setLangPersist = (l: string) => {
      const r = resolveLang(l);
      localStorage.setItem('rq_lang', r);
      setLang(r);
      api.updateMe({ lang: r }).catch(console.error);
    };
    return { lang, setLang: setLangPersist, t };
  }, [lang]);

  return <LangContext.Provider value={value}>{children}</LangContext.Provider>;
}

export const useLang = () => {
  const ctx = useContext(LangContext);
  if (!ctx) throw new Error("useLang must be used within LangProvider");
  return ctx;
};
