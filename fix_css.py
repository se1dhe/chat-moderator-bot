import re

css_path = 'webapp/src/styles/index.css'
with open(css_path, 'r') as f:
    css = f.read()

# Replace the :root block
new_root = """:root {
  /* Common */
  --nav-h: 62px;
  --safe-top: env(safe-area-inset-top, 0px);
  --safe-bottom: env(safe-area-inset-bottom, 0px);
  --radius: 16px;
  --radius-sm: 11px;
  --radius-lg: 22px;
  --transition: 0.18s cubic-bezier(0.4, 0, 0.2, 1);

  /* Dark Theme (Default) */
  --bg-base: #09090B;
  --bg-surface: #131316;
  --bg-card: rgba(255,255,255,0.04);
  --bg-card-hover: rgba(255,255,255,0.06);
  --bg-elevated: #1C1C21;

  --primary: #DC2626;
  --primary-light: #EF4444;
  --primary-dim: #991b1b;
  --primary-glow: rgba(220, 38, 38, 0.12);
  --primary-glow-strong: rgba(220, 38, 38, 0.30);
  --primary-border: rgba(220, 38, 38, 0.38);

  --gold: #EAB308;
  --gold-light: #FBBF24;
  --success: #22C55E;
  --success-glow: rgba(34, 197, 94, 0.15);
  --danger: #EF4444;
  --info: #3b82f6;

  --text-primary: #F4F4F5;
  --text-secondary: #D4D4D8;
  --text-muted: #71717A;

  --border: rgba(255, 255, 255, 0.08);
  --border-hover: rgba(255, 255, 255, 0.13);
  --glass-border: rgba(255,255,255,0.06);

  --shadow-card: 0 4px 28px rgba(0, 0, 0, 0.5);
  --shadow-glow: 0 0 40px rgba(220, 38, 38, 0.08);
}

:root.light {
  --bg-base: #FAFAFA;
  --bg-surface: #FFFFFF;
  --bg-card: rgba(0,0,0,0.02);
  --bg-card-hover: rgba(0,0,0,0.04);
  --bg-elevated: #F4F4F5;

  --primary: #DC2626;
  --primary-light: #B91C1C;
  --primary-dim: #7f1d1d;
  --primary-glow: rgba(220, 38, 38, 0.08);
  --primary-glow-strong: rgba(220, 38, 38, 0.20);
  --primary-border: rgba(220, 38, 38, 0.28);

  --gold: #CA8A04;
  --gold-light: #B45309;
  --success: #16A34A;
  --success-glow: rgba(22, 163, 74, 0.15);
  --danger: #DC2626;
  --info: #2563eb;

  --text-primary: #09090B;
  --text-secondary: #3F3F46;
  --text-muted: #71717A;

  --border: rgba(0, 0, 0, 0.08);
  --border-hover: rgba(0, 0, 0, 0.13);
  --glass-border: rgba(0,0,0,0.04);

  --shadow-card: 0 4px 28px rgba(0, 0, 0, 0.05);
  --shadow-glow: 0 0 40px rgba(220, 38, 38, 0.05);
}
"""

css = re.sub(r':root\s*\{[^}]+\}', new_root, css, count=1, flags=re.DOTALL)

# Add transition to everything for smooth theme switching
theme_transition = """
/* Smooth theme switching */
body {
  transition: background-color 0.3s ease, color 0.3s ease;
}
.card, .tile, .btn, .input, .bottom-nav, .app-header {
  transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease;
}
"""
css += theme_transition

with open(css_path, 'w') as f:
    f.write(css)

print("CSS rewritten")
