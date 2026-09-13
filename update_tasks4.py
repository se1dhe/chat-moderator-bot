with open('/Users/se1dhe/.gemini/antigravity/brain/8c432176-0233-49d1-9a21-7245ab971baf/task.md', 'r') as f:
    text = f.read()

text += """
### Phase 3: Killer Features
- [/] Network of Trust (Global Filters)
- [ ] AI Tribunal (Log Channel for Quarantine Voting)
- [ ] AI Summarizer (Daily/On-demand Digests)
"""

with open('/Users/se1dhe/.gemini/antigravity/brain/8c432176-0233-49d1-9a21-7245ab971baf/task.md', 'w') as f:
    f.write(text)
