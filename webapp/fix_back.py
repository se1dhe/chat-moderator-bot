import re

with open('src/components/TelegramBackButton.tsx', 'r') as f:
    text = f.read()

old_logic = """      const parts = location.pathname.split('/').filter(Boolean);
      if (parts.length === 2 || (parts.length === 3 && ['members', 'quarantine', 'audit', 'stats'].includes(parts[2]))) {
        navigate('/');
      } else {
        navigate(-1);
      }"""

new_logic = """      const parts = location.pathname.split('/').filter(Boolean);
      if (parts.length === 2) {
        navigate('/');
      } else if (parts.length === 3 && ['members', 'quarantine', 'audit', 'stats'].includes(parts[2])) {
        navigate(`/c/${parts[1]}`);
      } else {
        navigate(-1);
      }"""

text = text.replace(old_logic, new_logic)

with open('src/components/TelegramBackButton.tsx', 'w') as f:
    f.write(text)

