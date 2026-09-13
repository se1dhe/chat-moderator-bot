import { initData } from './telegram';
import { MeResponse, ChatSettingsData, AuditLog } from './types';

export const API_BASE = '/api';

interface RequestOpts {
  signal?: AbortSignal;
}

async function request<T>(method: string, path: string, body?: any, opts: RequestOpts = {}): Promise<T> {
  const headers: Record<string, string> = { Authorization: `tma ${initData}` };
  if (body !== undefined) headers['Content-Type'] = 'application/json';
  
  const resp = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
    signal: opts.signal,
  });
  
  if (!resp.ok) {
    let detail = resp.statusText;
    try { 
      const data = await resp.json();
      detail = data.error || detail;
    } catch { /* empty */ }
    const err = new Error(detail) as any;
    err.status = resp.status;
    throw err;
  }
  
  if (resp.status === 204) return null as any;
  return resp.json();
}

export const api = {
  me: () => request<MeResponse>("GET", "/me"),
  get: <T>(path: string, opts?: RequestOpts) => request<T>("GET", path, undefined, opts),
  post: <T>(path: string, body?: any, opts?: RequestOpts) => request<T>("POST", path, body, opts),
  del: <T>(path: string, opts?: RequestOpts) => request<T>("DELETE", path, undefined, opts),
  
  updateMe: (patch: any) => request<any>('PUT', '/me', patch),
  getSettings: (cid: number | string) => request<ChatSettingsData>('GET', `/chats/${cid}/settings`),
  putSettings: (cid: number | string, patch: Partial<ChatSettingsData>) => request<ChatSettingsData>('PUT', `/chats/${cid}/settings`, patch),
  
  audit: (cid: number | string, limit = 50, page = 1) => request<AuditLog[]>('GET', `/chats/${cid}/audit?limit=${limit}&page=${page}`),
  quarantine: (cid: number | string) => request<any[]>('GET', `/chats/${cid}/quarantine`),
  decide: (cid: number | string, vid: number | string, action: string) => request<any>('POST', `/chats/${cid}/quarantine/${vid}`, { action }),
  stats: (cid: number | string) => request<any>('GET', `/chats/${cid}/stats`),
  billing: (cid: number | string) => request<any>('GET', `/chats/${cid}/billing`),
  invoice: (cid: number | string, method = 'stars') => request<any>('POST', `/chats/${cid}/billing/invoice`, { method }),
  
  members: (cid: number | string, q = '', opts?: RequestOpts) => request<any[]>('GET', `/chats/${cid}/members?q=${encodeURIComponent(q)}`, undefined, opts),
  memberAction: (cid: number | string, uid: number | string, action: string, extra = {}) =>
    request<any>('POST', `/chats/${cid}/members/${uid}/action`, { action, ...extra }),
    
  triggers: (cid: number | string) => request<any[]>('GET', `/chats/${cid}/triggers`),
  createTrigger: (cid: number | string, data: any) => request<any>('POST', `/chats/${cid}/triggers`, data),
  deleteTrigger: (cid: number | string, tid: number | string) => request<any>('DELETE', `/chats/${cid}/triggers/${tid}`),
  
  uploadMedia: async (cid: number | string, file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const resp = await fetch(`${API_BASE}/chats/${cid}/upload`, {
      method: 'POST',
      headers: { Authorization: `tma ${initData}` },
      body: formData,
    });
    if (!resp.ok) throw new Error(await resp.text());
    return resp.json();
  }
};
