with open("webapp/src/pages/SettingsSection.jsx", "r") as f:
    text = f.read()

text = text.replace(
    "triggers: <Triggers chatId={s.chatId} t={t} />,",
    "triggers: <Triggers chatId={s.chatId} t={t} />,\n    welcome: <Welcome s={s} t={t} />,"
)

welcome_comp = """
function Welcome({ s, t }) {
  const msg = s.draft.onboarding?.welcome_message || ''
  return (
    <>
      <div className="section-label">{t('sec.welcome')}</div>
      <div className="card card-pad" style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
        <div className="row-desc">{t('welcome.desc')}</div>
        <div style={{ fontWeight: 600, fontSize: '15px', marginTop: '0.5rem' }}>{t('welcome.text')}</div>
        <textarea
          className="input"
          style={{ minHeight: '120px', resize: 'vertical' }}
          value={msg}
          placeholder={t('welcome.text.ph')}
          onChange={(e) => s.updateSection('onboarding', { welcome_message: e.target.value })}
        ></textarea>
      </div>
    </>
  )
}
"""

text = text + welcome_comp

with open("webapp/src/pages/SettingsSection.jsx", "w") as f:
    f.write(text)
