import re

with open('webapp/src/components/Layout.tsx', 'r') as f:
    text = f.read()

# Add useEffect for clearing audit badge when visiting audit page
if 'const { badges, clearAuditBadge } = useChatSettings();' not in text:
    nav_old = """function Nav({ cid }: { cid: string }) {
  const { t } = useLang();
  const base = `/c/${cid}`;
  const items = [
    { to: base, icon: LayoutGrid, label: t('nav.dashboard'), end: true },
    { to: `${base}/members`, icon: Users, label: t('nav.members') },
    { to: `${base}/quarantine`, icon: ShieldAlert, label: t('nav.quarantine') },
    { to: `${base}/audit`, icon: ScrollText, label: t('nav.audit') },
    { to: `${base}/stats`, icon: BarChart3, label: t('nav.stats') },
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-40 bg-white/90 dark:bg-black/80 backdrop-blur-2xl border-t border-neutral-200 dark:border-neutral-800/60 pb-safe">
      <div className="max-w-md mx-auto w-full flex items-center justify-between px-2 h-16">
        {items.map((it) => (
          <NavLink 
            key={it.to} 
            to={it.to} 
            end={it.end} 
            onClick={() => haptic('light')}
            className={({ isActive }) => `
              flex flex-col items-center justify-center w-full h-full gap-1 transition-colors
              ${isActive ? 'text-primary' : 'text-neutral-500 hover:text-neutral-900 dark:hover:text-neutral-300'}
            `}
          >
            {({ isActive }) => (
              <>
                <it.icon size={22} className={isActive ? 'fill-primary/10' : ''} />
                <span className="text-[10px] font-medium leading-none">{it.label}</span>
              </>
            )}
          </NavLink>
        ))}
      </div>
    </nav>
  );
}"""

    nav_new = """function Nav({ cid }: { cid: string }) {
  const { t } = useLang();
  const location = useLocation();
  const { badges, clearAuditBadge } = useChatSettings();
  const base = `/c/${cid}`;
  
  import { useEffect } from 'react';
  useEffect(() => {
    if (location.pathname.endsWith('/audit')) {
      clearAuditBadge();
    }
  }, [location.pathname, clearAuditBadge]);

  const items = [
    { to: base, icon: LayoutGrid, label: t('nav.dashboard'), end: true, badge: 0 },
    { to: `${base}/members`, icon: Users, label: t('nav.members'), badge: 0 },
    { to: `${base}/quarantine`, icon: ShieldAlert, label: t('nav.quarantine'), badge: badges?.quarantine || 0 },
    { to: `${base}/audit`, icon: ScrollText, label: t('nav.audit'), badge: badges?.audit || 0 },
    { to: `${base}/stats`, icon: BarChart3, label: t('nav.stats'), badge: 0 },
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-40 bg-white/90 dark:bg-black/80 backdrop-blur-2xl border-t border-neutral-200 dark:border-neutral-800/60 pb-safe">
      <div className="max-w-md mx-auto w-full flex items-center justify-between px-2 h-16">
        {items.map((it) => (
          <NavLink 
            key={it.to} 
            to={it.to} 
            end={it.end} 
            onClick={() => haptic('light')}
            className={({ isActive }) => `
              flex flex-col items-center justify-center w-full h-full gap-1 transition-colors relative
              ${isActive ? 'text-primary' : 'text-neutral-500 hover:text-neutral-900 dark:hover:text-neutral-300'}
            `}
          >
            {({ isActive }) => (
              <>
                <div className="relative">
                  <it.icon size={22} className={isActive ? 'fill-primary/10' : ''} />
                  {it.badge > 0 && (
                    <div className="absolute -top-1.5 -right-2 bg-red-500 text-white text-[9px] font-bold px-1.5 py-0.5 rounded-full border-2 border-white dark:border-black min-w-[18px] text-center shadow-sm">
                      {it.badge > 99 ? '99+' : it.badge}
                    </div>
                  )}
                </div>
                <span className="text-[10px] font-medium leading-none">{it.label}</span>
              </>
            )}
          </NavLink>
        ))}
      </div>
    </nav>
  );
}"""
    # Fix import useEffect if not in Layout.tsx
    if "import { useEffect" not in text and "useEffect," not in text:
        text = text.replace("import { NavLink,", "import { NavLink,") # Do not mess up import
    
    text = text.replace(nav_old, nav_new)

    # Need to make sure useEffect is actually imported at the top
    if 'useEffect' not in text.splitlines()[0] and 'useEffect' not in text.splitlines()[1]:
        text = text.replace("import { NavLink", "import { useEffect } from 'react';\nimport { NavLink")
        # Remove the nested import I added above
        text = text.replace("  import { useEffect } from 'react';\n", "")

with open('webapp/src/components/Layout.tsx', 'w') as f:
    f.write(text)
