with open('webapp/src/components/ui.tsx', 'r') as f:
    text = f.read()

# Add Info to lucide imports if not there
if 'Info,' not in text and 'Info } from' not in text:
    text = text.replace("import { motion", "import { Info } from 'lucide-react';\nimport { motion")

old_row = """export function Row({ title, desc, value, children }: { title: string, desc?: string, value?: any, children?: ReactNode }) {
  return (
    <div className="flex items-center justify-between w-full p-2 gap-3 min-h-[44px]">
      <div className="flex flex-col flex-1 min-w-0 justify-center">
        <div className="text-sm font-semibold text-neutral-900 dark:text-neutral-50 truncate leading-tight">{title}</div>"""

new_row = """export function Row({ title, desc, value, children, onInfo }: { title: string, desc?: string, value?: any, children?: ReactNode, onInfo?: () => void }) {
  return (
    <div className="flex items-center justify-between w-full p-2 gap-3 min-h-[44px]">
      <div className="flex flex-col flex-1 min-w-0 justify-center">
        <div className="text-sm font-semibold text-neutral-900 dark:text-neutral-50 truncate leading-tight flex items-center gap-1.5">
          {title}
          {onInfo && <button onClick={onInfo} className="text-neutral-400 hover:text-blue-500 active:scale-95 transition-all"><Info size={15} /></button>}
        </div>"""

text = text.replace(old_row, new_row)

with open('webapp/src/components/ui.tsx', 'w') as f:
    f.write(text)
