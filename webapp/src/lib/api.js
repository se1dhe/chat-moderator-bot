// API client — every request carries the Telegram initData for auth.
import { initData } from './telegram'

async function request(method, path, body, opts = {}) {
  const headers = { Authorization: `tma ${initData}` }
  if (body !== undefined) headers['Content-Type'] = 'application/json'
  const resp = await fetch(`/api${path}`, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
    signal: opts.signal,
  })
  if (!resp.ok) {
    let detail = resp.statusText
    try { detail = (await resp.json()).error || detail } catch { /* non-JSON */ }
    const err = new Error(detail)
    err.status = resp.status
    throw err
  }
  if (resp.status === 204) return null
  return resp.json()
}

export const api = {
  me: () => request('GET', '/me'),
  updateMe: (patch) => request('PUT', '/me', patch),
  getSettings: (cid) => request('GET', `/chats/${cid}/settings`),
  putSettings: (cid, patch) => request('PUT', `/chats/${cid}/settings`, patch),
  audit: (cid, limit = 50) => request('GET', `/chats/${cid}/audit?limit=${limit}`),
  quarantine: (cid) => request('GET', `/chats/${cid}/quarantine`),
  decide: (cid, vid, action) => request('POST', `/chats/${cid}/quarantine/${vid}`, { action }),
  stats: (cid) => request('GET', `/chats/${cid}/stats`),
  billing: (cid) => request('GET', `/chats/${cid}/billing`),
  invoice: (cid, method = 'stars') => request('POST', `/chats/${cid}/billing/invoice`, { method }),
  members: (cid, q = '', opts = {}) => request('GET', `/chats/${cid}/members?q=${encodeURIComponent(q)}`, undefined, opts),
  memberAction: (cid, uid, action, extra = {}) =>
    request('POST', `/chats/${cid}/members/${uid}/action`, { action, ...extra }),
  uploadMedia: async (cid, file) => {
    const formData = new FormData()
    formData.append('file', file)
    const resp = await fetch(`/api/chats/${cid}/upload`, {
      method: 'POST',
      headers: { Authorization: `tma ${initData}` },
      body: formData,
    })
    if (!resp.ok) throw new Error(await resp.text())
    return resp.json()
  }
}
