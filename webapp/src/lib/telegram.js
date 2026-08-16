// Thin wrapper over the Telegram WebApp SDK (loaded via index.html script tag).
const tg = window.Telegram?.WebApp

export function initTelegram() {
  if (!tg) return
  try {
    tg.ready()
    tg.expand()
    // RedQueen keeps its own dark-red identity regardless of the client theme.
    tg.setHeaderColor?.('#07070e')
    tg.setBackgroundColor?.('#07070e')
    tg.disableVerticalSwipes?.()
  } catch { /* older clients */ }
}

// In a production build import.meta.env.DEV is false, so this is only ever a local
// convenience for previewing the UI outside Telegram — it compiles away in prod.
export const initData =
  tg?.initData || (import.meta.env.DEV ? (import.meta.env.VITE_DEV_INIT_DATA || '') : '')

export function startParam() {
  return tg?.initDataUnsafe?.start_param || ''
}

export function tgUser() {
  return tg?.initDataUnsafe?.user || null
}

export function tgLang() {
  return tg?.initDataUnsafe?.user?.language_code || 'en'
}

export function haptic(type = 'light') {
  try {
    if (type === 'success' || type === 'error' || type === 'warning') {
      tg?.HapticFeedback?.notificationOccurred(type)
    } else {
      tg?.HapticFeedback?.impactOccurred(type)
    }
  } catch { /* no haptics */ }
}

export function showConfirm(message) {
  return new Promise((resolve) => {
    if (tg?.showConfirm) tg.showConfirm(message, resolve)
    else resolve(window.confirm(message))
  })
}

export function openInvoice(url) {
  return new Promise((resolve) => {
    if (tg?.openInvoice) tg.openInvoice(url, resolve)
    else { window.open(url, '_blank'); resolve('unknown') }
  })
}

export const isTelegram = Boolean(tg && tg.initData)
