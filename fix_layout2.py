with open("webapp/src/components/Layout.jsx", "r") as f:
    text = f.read()

text = text.replace(
    '<div className="subtitle">{s?.chat?.title || t(\'app.subtitle\')}</div>',
    '{!section && <div className="subtitle">{t(\'app.subtitle\')}</div>}'
)

with open("webapp/src/components/Layout.jsx", "w") as f:
    f.write(text)
