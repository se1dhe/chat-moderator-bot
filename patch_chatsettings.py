import re

with open('webapp/src/context/ChatSettingsContext.tsx', 'r') as f:
    text = f.read()

# Add badges to interface
if 'badges:' not in text:
    text = text.replace('pro: boolean;', 'pro: boolean;\n  badges: { quarantine: number; audit: number };\n  clearAuditBadge: () => void;')

# Add badges state
if 'const [badges, setBadges]' not in text:
    state_code = """
  const [badges, setBadges] = useState({ quarantine: 0, audit: 0 });
  const [totalActions, setTotalActions] = useState(0);

  useEffect(() => {
    let alive = true;
    const poll = async () => {
      try {
        const stats = await api.stats(chatId);
        if (alive && stats) {
          const qCount = stats.pending_quarantine || 0;
          const tActions = Object.values(stats.actions || {}).reduce((a: any, b: any) => a + b, 0) as number;
          setTotalActions(tActions);
          const lastSeen = parseInt(localStorage.getItem(`lastSeenActions_${chatId}`) || '0', 10);
          const aCount = Math.max(0, tActions - lastSeen);
          setBadges({ quarantine: qCount, audit: aCount });
        }
      } catch(e) {}
    };
    poll();
    const interval = setInterval(poll, 10000);
    return () => { alive = false; clearInterval(interval); };
  }, [chatId]);

  const clearAuditBadge = useCallback(() => {
    localStorage.setItem(`lastSeenActions_${chatId}`, totalActions.toString());
    setBadges(b => ({ ...b, audit: 0 }));
  }, [chatId, totalActions]);
"""
    text = text.replace('const [paymentResolver, setPaymentResolver] = useState<((val: string | null) => void) | null>(null);', 'const [paymentResolver, setPaymentResolver] = useState<((val: string | null) => void) | null>(null);\n' + state_code)

# Add to value object
if 'badges,' not in text:
    text = text.replace('billing, pro, loadBilling, openUpgrade', 'billing, pro, loadBilling, openUpgrade, badges, clearAuditBadge')
    text = text.replace('openUpgrade,\n  }), [', 'openUpgrade, badges, clearAuditBadge,\n  }), [')
    text = text.replace('loadBilling, openUpgrade]', 'loadBilling, openUpgrade, badges, clearAuditBadge]')

with open('webapp/src/context/ChatSettingsContext.tsx', 'w') as f:
    f.write(text)
