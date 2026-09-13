import re
with open('webapp/src/lib/api.ts', 'r') as f:
    text = f.read()

text = text.replace(
    "invoice: (cid: number | string, method = 'stars') => request<any>('POST', `/chats/${cid}/billing/invoice`, { method }),",
    "invoice: (cid: number | string, method = 'stars', preset_id?: string) => request<any>('POST', `/chats/${cid}/billing/invoice`, { method, preset_id }),"
)
with open('webapp/src/lib/api.ts', 'w') as f:
    f.write(text)
