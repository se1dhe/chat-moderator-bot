with open('/Users/se1dhe/.gemini/antigravity/brain/8c432176-0233-49d1-9a21-7245ab971baf/task.md', 'r') as f:
    text = f.read()

text = text.replace('- [/] Network of Trust (Global Filters)', '- [x] Network of Trust (Global Filters)')
text = text.replace('- [ ] AI Tribunal (Log Channel for Quarantine Voting)', '- [x] AI Tribunal (Log Channel for Quarantine Voting)')
text = text.replace('- [ ] AI Summarizer (Daily/On-demand Digests)', '- [x] AI Summarizer (Daily/On-demand Digests)')

with open('/Users/se1dhe/.gemini/antigravity/brain/8c432176-0233-49d1-9a21-7245ab971baf/task.md', 'w') as f:
    f.write(text)
