with open('/Users/se1dhe/.gemini/antigravity/brain/8c432176-0233-49d1-9a21-7245ab971baf/task.md', 'r') as f:
    text = f.read()

text = text.replace('- [ ] Design Auto-DEFCON mechanics', '- [x] Design Auto-DEFCON mechanics (Waiting for user confirmation)')
text = text.replace('- [ ] Backend: Rate limit tracking', '- [/] Backend: Rate limit tracking')

with open('/Users/se1dhe/.gemini/antigravity/brain/8c432176-0233-49d1-9a21-7245ab971baf/task.md', 'w') as f:
    f.write(text)
