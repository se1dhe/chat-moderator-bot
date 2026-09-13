with open('src/pages/settings/Welcome.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    'className="w-full flex items-center justify-center gap-2 py-3 bg-neutral-200 dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 rounded-xl font-bold transition-all active:scale-95 text-[15px] px-2.5 py-1 text-xs"',
    'className="shrink-0 flex items-center justify-center gap-1.5 px-3 py-1.5 bg-neutral-200 dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 rounded-lg font-bold transition-all active:scale-95 text-[12px]"'
)

with open('src/pages/settings/Welcome.tsx', 'w') as f:
    f.write(content)

print("Fixed Welcome!")
