filename = "webapp/src/pages/Triggers.jsx"
with open(filename, "r") as f:
    text = f.read()

text = text.replace("export default function Triggers({ chatId }) {", "export default function Triggers({ chatId, t }) {")
text = text.replace("<h2>Auto-Replies (Triggers)</h2>", "<h2>{t ? t('sec.triggers') : 'Auto-Replies'}</h2>")
text = text.replace('<h2 className="text-xl font-display font-bold">Auto-Replies (Triggers)</h2>', '<h2 className="text-xl font-display font-bold">{t ? t("sec.triggers") : "Auto-Replies"}</h2>')

with open(filename, "w") as f:
    f.write(text)
