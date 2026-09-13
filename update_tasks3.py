with open('/Users/se1dhe/.gemini/antigravity/brain/8c432176-0233-49d1-9a21-7245ab971baf/task.md', 'r') as f:
    text = f.read()

text = text.replace('- [/] Backend: Rate limit tracking', '- [x] Backend: Rate limit tracking')
text = text.replace('- [ ] Frontend: DEFCON tab in TMA', '- [x] Frontend: DEFCON tab in TMA')

with open('/Users/se1dhe/.gemini/antigravity/brain/8c432176-0233-49d1-9a21-7245ab971baf/task.md', 'w') as f:
    f.write(text)
