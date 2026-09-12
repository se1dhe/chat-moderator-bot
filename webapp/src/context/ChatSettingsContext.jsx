import { createContext, useCallback, useContext, useEffect, useRef, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { api } from '../lib/api'
import { haptic, openInvoice } from '../lib/telegram'

const Ctx = createContext(null)

const clone = (o) => JSON.parse(JSON.stringify(o))

// Autosave model: edits mutate the local draft immediately (optimistic) and a debounced
// flush persists the whole draft to the server. No save/cancel bar — settings are "live",
// which also kills the floating-bar repaint glitch on fast scroll. On failure we roll the
// draft back to the last server-confirmed state.
export function ChatSettingsProvider({ chatId, children }) {
  const [saved, setSaved] = useState(null)
  const [draft, setDraft] = useState(null)
  const [error, setError] = useState(null)
  const [saving, setSaving] = useState(false)
  const [billing, setBilling] = useState(null)  // { pro, active_until, price_stars, period_days, features }
  const [paymentResolver, setPaymentResolver] = useState(null)

  const draftRef = useRef(null)
  const savedRef = useRef(null)
  const timerRef = useRef(null)
  const patchRef = useRef({})

  const commit = (v) => { setSaved(v); savedRef.current = v; setDraft(clone(v)); draftRef.current = clone(v) }

  const load = useCallback(async () => {
    setError(null)
    try {
      commit(await api.getSettings(chatId))
    } catch (e) {
      setError(e)
    }
  }, [chatId])

  useEffect(() => { load() }, [load])

  const loadBilling = useCallback(() => {
    api.billing(chatId).then(setBilling).catch(() => {})
  }, [chatId])

  useEffect(() => { loadBilling() }, [loadBilling])

  // Open the Stars invoice for Pro; refresh entitlement on success. Shared by the Pro
  // banner and every Pro-locked control (locked cards, disabled toggles).
  const openUpgrade = useCallback(() => {
    return new Promise((resolve) => {
      haptic('light')
      setPaymentResolver(() => resolve)
    })
  }, [])

  const handlePaymentSelect = useCallback(async (method) => {
    const resolve = paymentResolver
    setPaymentResolver(null)
    if (!method) {
      resolve?.(null)
      return
    }

    try {
      if (method === 'crypto') {
        const data = await api.createInvoice(chatId, 'crypto')
        if (data.url) {
          window.Telegram?.WebApp?.openLink(data.url)
          resolve?.('crypto')
        }
      } else if (method === 'stars') {
        const data = await api.createInvoice(chatId, 'stars')
        if (data.url) {
          window.Telegram?.WebApp?.openInvoice(data.url, (status) => {
            if (status === 'paid') {
              loadBilling()
              resolve?.('stars')
            } else {
              resolve?.(null)
            }
          })
        }
      }
    } catch {
      haptic('error')
      resolve?.(null)
    }
  }, [chatId, loadBilling, paymentResolver])

  const flush = useCallback(async () => {
    const payload = patchRef.current
    if (Object.keys(payload).length === 0) return
    patchRef.current = {} // clear before request to queue any new edits
    setSaving(true)
    setError(null)
    try {
      const v = await api.putSettings(chatId, payload)
      setSaved(v)
      savedRef.current = v
      
      setDraft((_oldDraft) => {
        const latest = clone(v)
        // re-apply any edits that happened while request was in-flight
        for (const [k, val] of Object.entries(patchRef.current)) {
          if (typeof val === 'object' && !Array.isArray(val) && val !== null) {
            latest[k] = { ...latest[k], ...val }
          } else {
            latest[k] = val
          }
        }
        draftRef.current = latest
        return latest
      })
      haptic('success')
    } catch (e) {
      setError(e)
      haptic('error')
      // Restore patch queue on failure so it can be retried
      patchRef.current = { ...payload, ...patchRef.current }
    } finally {
      setSaving(false)
    }
  }, [chatId])

  const schedule = useCallback(() => {
    if (timerRef.current) clearTimeout(timerRef.current)
    timerRef.current = setTimeout(flush, 500)
  }, [flush])

  const updateSection = useCallback((section, patch) => {
    patchRef.current = { 
      ...patchRef.current, 
      [section]: { ...(patchRef.current[section] || {}), ...patch } 
    }
    setDraft((d) => {
      const next = { ...d, [section]: { ...d[section], ...patch } }
      draftRef.current = next
      return next
    })
    schedule()
  }, [schedule])

  const setSection = useCallback((section, value) => {
    patchRef.current = { ...patchRef.current, [section]: value }
    setDraft((d) => {
      const next = { ...d, [section]: value }
      draftRef.current = next
      return next
    })
    schedule()
  }, [schedule])

  useEffect(() => () => { if (timerRef.current) clearTimeout(timerRef.current) }, [])

  const pro = !!billing?.pro
  const value = {
    chatId, saved, draft, saving, error, updateSection, setSection, reload: load,
    billing, pro, loadBilling, openUpgrade,
  }
  return <Ctx.Provider value={value}>{children}</Ctx.Provider>
}

export const useChatSettings = () => useContext(Ctx)
