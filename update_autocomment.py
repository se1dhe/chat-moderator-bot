import sys

filename = "webapp/src/pages/SettingsSection.jsx"
with open(filename, "r") as f:
    text = f.read()

old_func = """function AutoComment({ s, t }) {
  const ac = s.draft.auto_comment
  return (
    <>
      <div className="section-label">{t('sec.autocomment')}</div>
      <div className="card">
        <Row title={t('autocomment.enabled')}>
          <Toggle checked={ac.enabled} onChange={(v) => s.updateSection('auto_comment', { enabled: v })} />
        </Row>
      </div>
      <div className="card" style={{ marginTop: '0.75rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        <div style={{ padding: '0.75rem 1rem' }}>
          <div style={{ fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.25rem' }}>{t('autocomment.text')}</div>
          <textarea
            className="input"
            rows={4}
            value={ac.text}
            onChange={(e) => s.updateSection('auto_comment', { text: e.target.value })}
          />
        </div>
        <div style={{ padding: '0 1rem 0.75rem' }}>
          <div style={{ fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.25rem' }}>{t('autocomment.media')}</div>
          <input
            className="input"
            type="url"
            value={ac.media_url}
            placeholder="https://..."
            onChange={(e) => s.updateSection('auto_comment', { media_url: e.target.value })}
          />
        </div>
      </div>
    </>
  )
}"""

new_func = """function AutoComment({ s, t }) {
  const ac = s.draft.auto_comment
  const ob = s.draft.onboarding || {}
  return (
    <>
      <div className="section-label">Welcome Message</div>
      <div className="card" style={{ marginBottom: '1.5rem', display: 'flex', flexDirection: 'column', gap: '0.5rem', padding: '1rem' }}>
        <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
          Sent when a new user joins. Supports <code>{'{name}'}</code> and <code>{'{chat}'}</code>. Leave empty to disable.
        </div>
        <textarea
          className="input"
          rows={3}
          value={ob.welcome_message || ''}
          placeholder="Welcome to {chat}, {name}!"
          onChange={(e) => s.updateSection('onboarding', { welcome_message: e.target.value })}
        />
      </div>

      <div className="section-label">{t('sec.autocomment')}</div>
      <div className="card">
        <Row title={t('autocomment.enabled')}>
          <Toggle checked={ac.enabled} onChange={(v) => s.updateSection('auto_comment', { enabled: v })} />
        </Row>
      </div>
      <div className="card" style={{ marginTop: '0.75rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        <div style={{ padding: '0.75rem 1rem' }}>
          <div style={{ fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.25rem' }}>{t('autocomment.text')}</div>
          <textarea
            className="input"
            rows={4}
            value={ac.text}
            onChange={(e) => s.updateSection('auto_comment', { text: e.target.value })}
          />
        </div>
        <div style={{ padding: '0 1rem 0.75rem' }}>
          <div style={{ fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.25rem' }}>{t('autocomment.media')}</div>
          <input
            className="input"
            type="url"
            value={ac.media_url}
            placeholder="https://..."
            onChange={(e) => s.updateSection('auto_comment', { media_url: e.target.value })}
          />
        </div>
      </div>
    </>
  )
}"""

text = text.replace(old_func, new_func)

with open(filename, "w") as f:
    f.write(text)
