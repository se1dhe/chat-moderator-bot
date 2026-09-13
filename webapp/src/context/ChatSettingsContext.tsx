import { createContext, useCallback, useContext, useEffect, useRef, useState, useMemo, ReactNode } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useLang } from './LangContext';
import { api } from '../lib/api';
import { haptic } from '../lib/telegram';
import { ChatSettingsData } from '../lib/types';

interface BillingData {
  pro: boolean;
  active_until?: string;
  price_stars?: number;
  period_days?: number;
  features?: string[];
}

interface ChatSettingsContextType {
  chatId: number;
  saved: ChatSettingsData | null;
  draft: ChatSettingsData | null;
  saving: boolean;
  error: any;
  updateSection: (section: keyof ChatSettingsData, patch: any) => void;
  setSection: (section: keyof ChatSettingsData, value: any) => void;
  reload: () => Promise<void>;
  billing: BillingData | null;
  pro: boolean;
  loadBilling: () => void;
  openUpgrade: () => Promise<string | null>;
}

const Ctx = createContext<ChatSettingsContextType | null>(null);

const clone = <T,>(o: T): T => JSON.parse(JSON.stringify(o));

export function ChatSettingsProvider({ chatId, children }: { chatId: number; children: ReactNode }) {
  const { t } = useLang();
  const [saved, setSaved] = useState<ChatSettingsData | null>(null);
  const [draft, setDraft] = useState<ChatSettingsData | null>(null);
  const [error, setError] = useState<any>(null);
  const [saving, setSaving] = useState(false);
  const [billing, setBilling] = useState<BillingData | null>(null);
  const [paymentResolver, setPaymentResolver] = useState<((val: string | null) => void) | null>(null);

  const draftRef = useRef<ChatSettingsData | null>(null);
  const savedRef = useRef<ChatSettingsData | null>(null);
  const timerRef = useRef<any>(null);
  const patchRef = useRef<Partial<ChatSettingsData>>({});

  const commit = (v: ChatSettingsData) => { 
    setSaved(v); savedRef.current = v; 
    setDraft(clone(v)); draftRef.current = clone(v); 
  };

  const load = useCallback(async () => {
    setError(null);
    try {
      commit(await api.getSettings(chatId));
    } catch (e) {
      setError(e);
    }
  }, [chatId]);

  useEffect(() => { load(); }, [load]);

  const loadBilling = useCallback(() => {
    api.billing(chatId).then(setBilling).catch(() => {});
  }, [chatId]);

  useEffect(() => { loadBilling(); }, [loadBilling]);

  const openUpgrade = useCallback(() => {
    return new Promise<string | null>((resolve) => {
      haptic('light');
      setPaymentResolver(() => resolve);
    });
  }, []);

  const handlePaymentSelect = useCallback(async (method: string | null) => {
    const resolve = paymentResolver;
    setPaymentResolver(null);
    if (!method) {
      resolve?.(null);
      return;
    }

    try {
      if (method === 'crypto') {
        const data = await api.invoice(chatId, 'crypto');
        if (data.url) {
          window.Telegram?.WebApp?.openLink(data.url);
          resolve?.('crypto');
        }
      } else if (method === 'stars') {
        const data = await api.invoice(chatId, 'stars');
        if (data.url) {
          window.Telegram?.WebApp?.openInvoice(data.url, (status: string) => {
            if (status === 'paid') {
              loadBilling();
              resolve?.('stars');
            } else {
              resolve?.(null);
            }
          });
        }
      }
    } catch {
      haptic('error');
      resolve?.(null);
    }
  }, [chatId, loadBilling, paymentResolver]);

  const flush = useCallback(async () => {
    const payload = patchRef.current;
    if (Object.keys(payload).length === 0) return;
    patchRef.current = {}; 
    setSaving(true);
    setError(null);
    try {
      const v = await api.putSettings(chatId, payload);
      setSaved(v);
      savedRef.current = v;
      
      setDraft((oldDraft) => {
        const latest = clone(v);
        for (const [k, val] of Object.entries(patchRef.current)) {
          const key = k as keyof ChatSettingsData;
          if (typeof val === 'object' && !Array.isArray(val) && val !== null) {
            (latest[key] as any) = { ...(latest[key] as any), ...val };
          } else {
            (latest[key] as any) = val;
          }
        }
        draftRef.current = latest;
        return latest;
      });
      haptic('success');
    } catch (e) {
      setError(e);
      haptic('error');
      patchRef.current = { ...payload, ...patchRef.current };
    } finally {
      setSaving(false);
    }
  }, [chatId]);

  const schedule = useCallback(() => {
    if (timerRef.current) clearTimeout(timerRef.current);
    timerRef.current = setTimeout(flush, 500);
  }, [flush]);

  const updateSection = useCallback((section: keyof ChatSettingsData, patch: any) => {
    patchRef.current = { 
      ...patchRef.current, 
      [section]: { ...(patchRef.current[section] as any || {}), ...patch } 
    };
    setDraft((d) => {
      if (!d) return d;
      const next = { ...d, [section]: { ...(d[section] as any), ...patch } };
      draftRef.current = next;
      return next;
    });
    schedule();
  }, [schedule]);

  const setSection = useCallback((section: keyof ChatSettingsData, value: any) => {
    patchRef.current = { ...patchRef.current, [section]: value };
    setDraft((d) => {
      if (!d) return d;
      const next = { ...d, [section]: value };
      draftRef.current = next;
      return next;
    });
    schedule();
  }, [schedule]);

  useEffect(() => () => { if (timerRef.current) clearTimeout(timerRef.current); }, []);

  const pro = !!billing?.pro;
  const value: ChatSettingsContextType = useMemo(() => ({
    chatId, saved, draft, saving, error, updateSection, setSection, reload: load,
    billing, pro, loadBilling, openUpgrade,
  }), [chatId, saved, draft, saving, error, updateSection, setSection, load, billing, pro, loadBilling, openUpgrade]);

  return (
    <Ctx.Provider value={value}>
      {children}
      <AnimatePresence>
        {paymentResolver && (
          <motion.div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-end" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onClick={() => handlePaymentSelect(null)}>
            <motion.div className="w-full bg-surface rounded-t-3xl p-6 pb-8 shadow-2xl flex flex-col items-center" initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }} transition={{ type: 'spring', damping: 25, stiffness: 200 }} onClick={e => e.stopPropagation()}>
              <div className="w-9 h-1.5 bg-white/20 rounded-full mb-5" />
              <h3 className="text-xl font-bold mb-2 text-neutral-900 dark:text-neutral-50">{t('pay.title')}</h3>
              <div className="text-sm text-neutral-500 mb-6 text-center">{t("pay.subtitle")}</div>
              <div className="w-full flex flex-col gap-3">
                <button className="flex items-center p-4 rounded-2xl border border-amber-500/30 bg-neutral-100 dark:bg-neutral-900 hover:bg-amber-500/10 transition-colors w-full" onClick={() => handlePaymentSelect('stars')}>
                  <div className="text-2xl mr-4 w-10 h-10 flex items-center justify-center bg-white/5 rounded-xl">⭐️</div>
                  <div className="flex flex-col items-start">
                    <div className="font-semibold text-neutral-900 dark:text-neutral-50">{t("pay.stars.title")}</div>
                    <div className="text-sm text-neutral-500 mt-0.5">{t("pay.stars.desc")}</div>
                  </div>
                </button>
                <button className="flex items-center p-4 rounded-2xl border border-blue-500/30 bg-neutral-100 dark:bg-neutral-900 hover:bg-blue-500/10 transition-colors w-full" onClick={() => handlePaymentSelect('crypto')}>
                  <div className="text-2xl mr-4 w-10 h-10 flex items-center justify-center bg-white/5 rounded-xl">💎</div>
                  <div className="flex flex-col items-start">
                    <div className="font-semibold text-neutral-900 dark:text-neutral-50">{t("pay.crypto.title")}</div>
                    <div className="text-sm text-neutral-500 mt-0.5">{t("pay.crypto.desc")}</div>
                  </div>
                </button>
              </div>
              <button className="mt-5 bg-transparent border-none text-neutral-500 font-semibold p-3 w-full rounded-xl hover:bg-white/5 transition-colors" onClick={() => handlePaymentSelect(null)}>{t("common.cancel")}</button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </Ctx.Provider>
  );
}

export const useChatSettings = () => {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("useChatSettings must be used within ChatSettingsProvider");
  return ctx;
};
