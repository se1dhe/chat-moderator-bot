import re

path = 'webapp/src/pages/Landing.jsx'
with open(path, 'r') as f:
    c = f.read()

replacements = [
    (r"'#07070e'", "'var(--bg-base)'"),
    (r"color: '#fff'", "color: 'var(--text-primary)'"),
    (r"color: '#9ca3af'", "color: 'var(--text-muted)'"),
    (r"color: '#ef4444'", "color: 'var(--primary)'"),
    (r"background: '#ef4444'", "background: 'var(--primary)'"),
    (r"background: '#000'", "background: 'var(--bg-elevated)'"),
    (r"rgba\(255,255,255,0\.02\)", "var(--bg-card)"),
    (r"rgba\(255,255,255,0\.03\)", "var(--bg-card)"),
    (r"rgba\(255,255,255,0\.05\)", "var(--glass-border)"),
    (r"rgba\(255,255,255,0\.1\)", "var(--border)"),
    (r"rgba\(239, 68, 68, 0\.1\)", "var(--primary-glow)"),
    (r"rgba\(239,68,68,0\.3\)", "var(--primary-border)"),
    (r"'#22c55e'", "'var(--success)'"),
    (r"rgba\(34, 197, 94, 0\.1\)", "var(--success-glow)"),
    (r"color: '#6b7280'", "color: 'var(--text-subtle)'"),
]

for old, new in replacements:
    c = re.sub(old, new, c)

with open(path, 'w') as f:
    f.write(c)

print("Landing patched")
