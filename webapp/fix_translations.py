import sys

content = open('src/i18n/translations.ts').read()

header = """export type LocaleDict = Record<string, string>;
export type Locales = 'en' | 'ru' | 'uk';
"""

if "export type LocaleDict" not in content:
    content = header + "\n" + content.replace("export const LOCALES = {", "export const LOCALES: Record<Locales, LocaleDict> = {")
    content = content.replace("export function resolveLang(code) {", "export function resolveLang(code: string): Locales {")
    
open('src/i18n/translations.ts', 'w').write(content)
