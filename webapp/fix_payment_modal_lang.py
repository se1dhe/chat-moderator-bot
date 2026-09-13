import re

with open("src/context/ChatSettingsContext.jsx", "r") as f:
    content = f.read()

content = content.replace("import { motion, AnimatePresence } from 'framer-motion'", "import { motion, AnimatePresence } from 'framer-motion'\nimport { useLang } from './LangContext'")

content = content.replace("export function ChatSettingsProvider({ chatId, children }) {", "export function ChatSettingsProvider({ chatId, children }) {\n  const { t } = useLang()")

content = content.replace("<h3>Choose Payment Method</h3>", "<h3>{t('pay.title')}</h3>")
content = content.replace('<div className="payment-modal-subtitle">How would you like to pay for RedQueen Pro?</div>', '<div className="payment-modal-subtitle">{t("pay.subtitle")}</div>')
content = content.replace('<div className="payment-title">Telegram Stars</div>', '<div className="payment-title">{t("pay.stars.title")}</div>')
content = content.replace('<div className="payment-desc">Fast and native payment</div>', '<div className="payment-desc">{t("pay.stars.desc")}</div>')
content = content.replace('<div className="payment-title">Crypto Pay</div>', '<div className="payment-title">{t("pay.crypto.title")}</div>')
content = content.replace('<div className="payment-desc">TON, USDT, BTC, ETH</div>', '<div className="payment-desc">{t("pay.crypto.desc")}</div>')
content = content.replace('<button className="payment-cancel" onClick={() => handlePaymentSelect(null)}>Cancel</button>', '<button className="payment-cancel" onClick={() => handlePaymentSelect(null)}>{t("common.cancel")}</button>')

with open("src/context/ChatSettingsContext.jsx", "w") as f:
    f.write(content)

tips = {
    'pay.title': ['Choose Payment Method', 'Выберите способ оплаты', 'Виберіть спосіб оплати'],
    'pay.subtitle': ['How would you like to pay for RedQueen Pro?', 'Как вы хотите оплатить RedQueen Pro?', 'Як ви хочете оплатити RedQueen Pro?'],
    'pay.stars.title': ['Telegram Stars', 'Telegram Stars', 'Telegram Stars'],
    'pay.stars.desc': ['Fast and native payment', 'Быстрая и нативная оплата', 'Швидка та нативна оплата'],
    'pay.crypto.title': ['Crypto Pay', 'Crypto Pay', 'Crypto Pay'],
    'pay.crypto.desc': ['TON, USDT, BTC, ETH', 'TON, USDT, BTC, ETH', 'TON, USDT, BTC, ETH'],
}

with open("src/i18n/translations.js", "r") as f:
    t_content = f.read()

def insert_keys(lang_content, lang_idx):
    lines = []
    for k, v in tips.items():
        val = v[lang_idx].replace("'", "\\'")
        lines.append(f"    '{k}': '{val}',")
    return "\n".join(lines) + "\n"

en_part = re.search(r'(en: \{)(.*?)(  \},)', t_content, re.DOTALL)
ru_part = re.search(r'(ru: \{)(.*?)(  \},)', t_content, re.DOTALL)
uk_part = re.search(r'(uk: \{)(.*?)(  \})', t_content, re.DOTALL)

t_content = t_content.replace(en_part.group(1) + en_part.group(2), en_part.group(1) + "\n" + insert_keys(en_part.group(2), 0) + en_part.group(2))
t_content = t_content.replace(ru_part.group(1) + ru_part.group(2), ru_part.group(1) + "\n" + insert_keys(ru_part.group(2), 1) + ru_part.group(2))
t_content = t_content.replace(uk_part.group(1) + uk_part.group(2), uk_part.group(1) + "\n" + insert_keys(uk_part.group(2), 2) + uk_part.group(2))

with open("src/i18n/translations.js", "w") as f:
    f.write(t_content)
