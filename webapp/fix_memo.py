import re

with open('src/context/ChatSettingsContext.tsx', 'r') as f:
    text = f.read()

old_val = """  const pro = !!billing?.pro;
  const value: ChatSettingsContextType = {
    chatId, saved, draft, saving, error, updateSection, setSection, reload: load,
    billing, pro, loadBilling, openUpgrade,
  };"""

new_val = """  const pro = !!billing?.pro;
  const value: ChatSettingsContextType = useMemo(() => ({
    chatId, saved, draft, saving, error, updateSection, setSection, reload: load,
    billing, pro, loadBilling, openUpgrade,
  }), [chatId, saved, draft, saving, error, updateSection, setSection, load, billing, pro, loadBilling, openUpgrade]);"""

text = text.replace(old_val, new_val)
text = text.replace("import { createContext, useContext", "import { createContext, useContext, useMemo")

with open('src/context/ChatSettingsContext.tsx', 'w') as f:
    f.write(text)

