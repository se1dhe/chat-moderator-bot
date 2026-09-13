with open('/Users/se1dhe/.gemini/antigravity/brain/8c432176-0233-49d1-9a21-7245ab971baf/task.md', 'r') as f:
    text = f.read()

text = text.replace('- [ ] Propagate backend error reasons', '- [x] Propagate backend error reasons')
text = text.replace('- [ ] Replace `alert()`/`confirm()`', '- [x] Replace `alert()`/`confirm()`')
text = text.replace('- [ ] Add `useMemo` to `ChatSettingsProvider`', '- [x] Add `useMemo` to `ChatSettingsProvider`')
text = text.replace('- [ ] Fix NaN math crashes in `Antiflood.tsx`', '- [x] Fix NaN math crashes in `Antiflood.tsx`')
text = text.replace('- [ ] Clean up hardcoded RU text in `RBAC.tsx`', '- [x] Clean up hardcoded RU text in `RBAC.tsx`')
text = text.replace('- [ ] Fix Back Button routing state', '- [x] Fix Back Button routing state')

with open('/Users/se1dhe/.gemini/antigravity/brain/8c432176-0233-49d1-9a21-7245ab971baf/task.md', 'w') as f:
    f.write(text)
