import re

with open('src/lib/api.ts', 'r') as f:
    text = f.read()

new_api = """  async updateMe(data: any) {
    return _fetch(`/me`, { method: 'PATCH', body: JSON.stringify(data) });
  },
  async getAvatarBlob(cid: number) {
    const resp = await fetch(`${API_BASE}/chats/${cid}/avatar`, {
      headers: { Authorization: `tma ${initData}` }
    });
    if (!resp.ok) throw new Error('no avatar');
    const blob = await resp.blob();
    return URL.createObjectURL(blob);
  },"""
text = text.replace("  async updateMe(data: any) {\n    return _fetch(`/me`, { method: 'PATCH', body: JSON.stringify(data) });\n  },", new_api)

with open('src/lib/api.ts', 'w') as f:
    f.write(text)

with open('src/pages/ChatPicker.tsx', 'r') as f:
    text = f.read()

old_avatar = """export function ChatAvatar({ cid, type }: { cid: number; type: string }) {
  const [error, setError] = useState(false);
  const Ico = typeIcon(type);
  if (error) return <div className="w-full h-full flex items-center justify-center bg-neutral-100 dark:bg-neutral-800 text-neutral-500"><Ico size={20} /></div>;
  return <img src={`/api/chats/${cid}/avatar`} onError={() => setError(true)} className="w-full h-full object-cover" />;
}"""

new_avatar = """export function ChatAvatar({ cid, type }: { cid: number; type: string }) {
  const [url, setUrl] = useState<string | null>(null);
  const [error, setError] = useState(false);
  const Ico = typeIcon(type);

  useEffect(() => {
    let active = true;
    api.getAvatarBlob(cid).then(blobUrl => {
      if (active) setUrl(blobUrl);
    }).catch(() => {
      if (active) setError(true);
    });
    return () => { active = false; };
  }, [cid]);

  if (error || !url) return <div className="w-full h-full flex items-center justify-center bg-neutral-100 dark:bg-neutral-800 text-neutral-500"><Ico size={20} /></div>;
  return <img src={url} className="w-full h-full object-cover" />;
}"""
text = text.replace(old_avatar, new_avatar)

with open('src/pages/ChatPicker.tsx', 'w') as f:
    f.write(text)

