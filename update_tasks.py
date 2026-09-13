with open('/Users/se1dhe/.gemini/antigravity/brain/8c432176-0233-49d1-9a21-7245ab971baf/task.md', 'r') as f:
    text = f.read()

text = text.replace('- [ ] Fix AI Semaphore Timeout', '- [x] Fix AI Semaphore Timeout')
text = text.replace('- [ ] Fix AI Rule Generation string', '- [x] Fix AI Rule Generation string')
text = text.replace('- [ ] Fix Admin PM Spam blocking', '- [x] Fix Admin PM Spam blocking')
text = text.replace('- [ ] Fix Unmute permissions reset', '- [x] Fix Unmute permissions reset')
text = text.replace('- [ ] Fix Webhook Race Condition', '- [x] Fix Webhook Race Condition')
text = text.replace('- [ ] Implement True DB Healthcheck', '- [x] Implement True DB Healthcheck')
text = text.replace('- [ ] Fix ClientSession memory leak', '- [x] Fix ClientSession memory leak')
text = text.replace('- [ ] Fix GlobalBan Postgres NULL', '- [x] Fix GlobalBan Postgres NULL')

with open('/Users/se1dhe/.gemini/antigravity/brain/8c432176-0233-49d1-9a21-7245ab971baf/task.md', 'w') as f:
    f.write(text)
