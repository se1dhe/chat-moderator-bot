// API client — every request carries the Telegram initData for auth.
import { initData } from './telegram'

async function request(method, path, body) {
  const headers = { Authorization: `tma ${initData}` }
  if (body !== undefined) headers['Content-Type'] = 'application/json'
  const resp = await fetch(`/api${path}`, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
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
  getSettings: (cid) => request('GET', `/chats/${cid}/settings`),
  putSettings: (cid, patch) => request('PUT', `/chats/${cid}/settings`, patch),
  audit: (cid, limit = 50) => request('GET', `/chats/${cid}/audit?limit=${limit}`),
  quarantine: (cid) => request('GET', `/chats/${cid}/quarantine`),
  decide: (cid, vid, action) => request('POST', `/chats/${cid}/quarantine/${vid}`, { action }),
  stats: (cid) => request('GET', `/chats/${cid}/stats`),
  billing: (cid) => request('GET', `/chats/${cid}/billing`),
  invoice: (cid) => request('POST', `/chats/${cid}/billing/invoice`),
}
