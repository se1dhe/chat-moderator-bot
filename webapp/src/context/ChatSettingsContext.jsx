import { createContext, useCallback, useContext, useEffect, useRef, useState } from 'react'
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

  const draftRef = useRef(null)
  const savedRef = useRef(null)
  const timerRef = useRef(null)

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
  const openUpgrade = useCallback(async () => {
    haptic('light')
    try {
      const { url } = await api.invoice(chatId)
      const status = await openInvoice(url)
      if (status === 'paid') { haptic('success'); loadBilling() }
      return status
    } catch {
      haptic('error')
    }
  }, [chatId, loadBilling])

  const flush = useCallback(async () => {
    const payload = draftRef.current
    if (!payload) return
    setSaving(true)
    setError(null)
    try {
      const v = await api.putSettings(chatId, payload)
      setSaved(v)
      savedRef.current = v
      // Re-sync the draft to the server's validated view (range clamps applied), but only
      // if the user hasn't kept editing while the request was in flight.
      if (JSON.stringify(draftRef.current) === JSON.stringify(payload)) {
        setDraft(clone(v))
        draftRef.current = clone(v)
      }
      haptic('success')
    } catch (e) {
      setError(e)
      haptic('error')
      if (savedRef.current) { setDraft(clone(savedRef.current)); draftRef.current = clone(savedRef.current) }
    } finally {
      setSaving(false)
    }
  }, [chatId])

  const schedule = useCallback(() => {
    if (timerRef.current) clearTimeout(timerRef.current)
    timerRef.current = setTimeout(flush, 500)
  }, [flush])

  const updateSection = useCallback((section, patch) => {
    setDraft((d) => {
      const next = { ...d, [section]: { ...d[section], ...patch } }
      draftRef.current = next
      return next
    })
    schedule()
  }, [schedule])

  const setSection = useCallback((section, value) => {
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
