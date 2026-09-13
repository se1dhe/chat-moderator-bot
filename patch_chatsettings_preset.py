import re

with open('webapp/src/context/ChatSettingsContext.tsx', 'r') as f:
    text = f.read()

# Add openPresetPayment to interface
text = text.replace(
    'openUpgrade: () => Promise<string | null>;\n}', 
    'openUpgrade: () => Promise<string | null>;\n  openPresetPayment: (presetId: string) => Promise<string | null>;\n}'
)

# Add state for preset payment
text = text.replace(
    'const [paymentResolver, setPaymentResolver] = useState<((val: string | null) => void) | null>(null);',
    'const [paymentResolver, setPaymentResolver] = useState<((val: string | null) => void) | null>(null);\n  const [paymentPresetId, setPaymentPresetId] = useState<string | null>(null);'
)

# Add openPresetPayment function
open_upgrade_code = """  const openUpgrade = useCallback(() => {
    return new Promise<string | null>((resolve) => {
      haptic('light');
      setPaymentPresetId(null);
      setPaymentResolver(() => resolve);
    });
  }, []);

  const openPresetPayment = useCallback((presetId: string) => {
    return new Promise<string | null>((resolve) => {
      haptic('light');
      setPaymentPresetId(presetId);
      setPaymentResolver(() => resolve);
    });
  }, []);"""

text = re.sub(
    r'  const openUpgrade = useCallback\(\(\) => \{.+?\}, \[\]\);',
    open_upgrade_code,
    text,
    flags=re.DOTALL
)

# Update handlePaymentSelect to use paymentPresetId
old_handle = """  const handlePaymentSelect = useCallback(async (method: string | null) => {
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
  }, [chatId, loadBilling, paymentResolver]);"""

new_handle = """  const handlePaymentSelect = useCallback(async (method: string | null) => {
    const resolve = paymentResolver;
    const presetId = paymentPresetId;
    setPaymentResolver(null);
    setPaymentPresetId(null);
    
    if (!method) {
      resolve?.(null);
      return;
    }

    try {
      if (method === 'crypto') {
        const data = await api.invoice(chatId, 'crypto', presetId || undefined);
        if (data.url) {
          window.Telegram?.WebApp?.openLink(data.url);
          resolve?.('crypto');
        }
      } else if (method === 'stars') {
        const data = await api.invoice(chatId, 'stars', presetId || undefined);
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
  }, [chatId, loadBilling, paymentResolver, paymentPresetId]);"""
text = text.replace(old_handle, new_handle)

# Expose openPresetPayment
text = text.replace('loadBilling, openUpgrade, badges', 'loadBilling, openUpgrade, openPresetPayment, badges')
text = text.replace('loadBilling, openUpgrade, openPresetPayment, openPresetPayment', 'loadBilling, openUpgrade, openPresetPayment')

with open('webapp/src/context/ChatSettingsContext.tsx', 'w') as f:
    f.write(text)
