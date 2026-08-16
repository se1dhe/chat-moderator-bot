import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import { api } from '../lib/api'
import { haptic } from '../lib/telegram'

const Ctx = createContext(null)

const clone = (o) => JSON.parse(JSON.stringify(o))

export function ChatSettingsProvider({ chatId, children }) {
  const [saved, setSaved] = useState(null)
  const [draft, setDraft] = useState(null)
  const [error, setError] = useState(null)
  const [saving, setSaving] = useState(false)

  const load = useCallback(async () => {
    setError(null)
    try {
      const v = await api.getSettings(chatId)
      setSaved(v)
      setDraft(clone(v))
    } catch (e) {
      setError(e)
    }
  }, [chatId])

  useEffect(() => { load() }, [load])

  const updateSection = useCallback((section, patch) => {
    setDraft((d) => ({ ...d, [section]: { ...d[section], ...patch } }))
  }, [])

  const setSection = useCallback((section, value) => {
    setDraft((d) => ({ ...d, [section]: value }))
  }, [])

  const dirty = useMemo(
    () => draft && saved && JSON.stringify(draft) !== JSON.stringify(saved),
    [draft, saved],
  )

  const save = useCallback(async () => {
    setSaving(true)
    setError(null)
    try {
      const v = await api.putSettings(chatId, draft)
      setSaved(v)
      setDraft(clone(v))
      haptic('success')
    } catch (e) {
      setError(e)
      haptic('error')
    } finally {
      setSaving(false)
    }
  }, [chatId, draft])

  const reset = useCallback(() => setDraft(clone(saved)), [saved])

  const value = { chatId, saved, draft, dirty, saving, error, updateSection, setSection, save, reset, reload: load }
  return <Ctx.Provider value={value}>{children}</Ctx.Provider>
}

export const useChatSettings = () => useContext(Ctx)
