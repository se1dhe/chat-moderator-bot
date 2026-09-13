declare global {
  interface Window {
    Telegram?: {
      WebApp: any;
    };
  }
}

const tg = window.Telegram?.WebApp;

export function initTelegram() {
  if (!tg) return;
  try {
    tg.ready();
    tg.expand();
    tg.disableVerticalSwipes?.();
  } catch { /* older clients */ }
}

export const initData: string =
  tg?.initData || (import.meta.env.DEV ? (import.meta.env.VITE_DEV_INIT_DATA || '') : '');

export function startParam(): string {
  return tg?.initDataUnsafe?.start_param || '';
}

export function tgUser(): any {
  return tg?.initDataUnsafe?.user || null;
}

export function tgLang(): string {
  return tg?.initDataUnsafe?.user?.language_code || 'en';
}

export function haptic(type: 'light' | 'medium' | 'heavy' | 'rigid' | 'soft' | 'success' | 'warning' | 'error' = 'light') {
  try {
    if (type === 'success' || type === 'error' || type === 'warning') {
      tg?.HapticFeedback?.notificationOccurred(type);
    } else {
      tg?.HapticFeedback?.impactOccurred(type);
    }
  } catch { /* no haptics */ }
}

export function showConfirm(message: string): Promise<boolean> {
  return new Promise((resolve) => {
    if (tg?.showConfirm) {
      tg.showConfirm(message, resolve);
    } else {
      resolve(window.confirm(message));
    }
  });
}

export function showAlert(message: string): Promise<void> {
  return new Promise((resolve) => {
    if (tg?.showAlert) {
      tg.showAlert(message, resolve);
    } else {
      window.alert(message);
      resolve();
    }
  });
}

export function openInvoice(url: string): Promise<string> {
  return new Promise((resolve) => {
    if (tg?.openInvoice) {
      tg.openInvoice(url, resolve);
    } else {
      window.open(url, '_blank');
      resolve('unknown');
    }
  });
}

export function openTelegramLink(url: string) {
  if (tg?.openTelegramLink) {
    tg.openTelegramLink(url);
  } else {
    window.open(url, '_blank');
  }
}

export const isTelegram = Boolean(tg && tg.initData);
