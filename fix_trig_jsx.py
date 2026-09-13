with open("webapp/src/pages/Triggers.jsx", "r") as f:
    t = f.read()

t = t.replace('<p className="text-sm text-[var(--tg-theme-hint-color)]">Configure the bot to reply automatically to specific phrases or commands.</p>', '<p className="text-sm text-[var(--tg-theme-hint-color)]">{t("triggers.desc")}</p>')

t = t.replace('<h3 className="font-bold text-sm">Add New Trigger</h3>', '<h3 className="font-bold text-sm">{t("triggers.add")}</h3>')

t = t.replace('<div className="text-sm font-medium">Phrase or Command</div>', '<div className="text-sm font-medium">{t("triggers.phrase")}</div>')
t = t.replace('placeholder="e.g. /rules or price"', 'placeholder={t("triggers.phrase.ph")}')

t = t.replace('<div className="text-sm font-medium">Reply Text</div>', '<div className="text-sm font-medium">{t("triggers.reply")}</div>')
t = t.replace('placeholder="The bot will send this..."', 'placeholder={t("triggers.reply.ph")}')

t = t.replace('<span className="text-sm">Use Regex</span>', '<span className="text-sm">{t("triggers.regex")}</span>')

t = t.replace('>\\n          Add Trigger\\n        </button>', '>\\n          {t("triggers.btn.add")}\\n        </button>')

t = t.replace('<h3 className="font-bold text-sm">Active Triggers</h3>', '<h3 className="font-bold text-sm">{t("triggers.active")}</h3>')

t = t.replace('<div className="text-sm text-[var(--tg-theme-hint-color)]">No triggers found.</div>', '<div className="text-sm text-[var(--tg-theme-hint-color)]">{t("triggers.empty")}</div>')

t = t.replace('>Delete</button>', '>{t("triggers.btn.delete")}</button>')

with open("webapp/src/pages/Triggers.jsx", "w") as f:
    f.write(t)
