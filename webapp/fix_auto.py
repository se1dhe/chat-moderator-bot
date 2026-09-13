with open('src/pages/settings/AutoComment.tsx', 'r') as f:
    content = f.read()

content = content.replace("text-[var(--tg-theme-text-color)]", "text-neutral-900 dark:text-neutral-50")
content = content.replace("text-[var(--tg-theme-hint-color)]", "text-neutral-500")

# Fix button padding
content = content.replace("px-4 py-2 bg-neutral-200 dark:bg-neutral-800 hover:bg-neutral-300 dark:hover:bg-neutral-700 text-neutral-900 dark:text-neutral-50 rounded-xl font-medium transition-colors px-3 py-1 text-[13px]", "px-4 py-2 bg-neutral-200 dark:bg-neutral-800 hover:bg-neutral-300 dark:hover:bg-neutral-700 text-neutral-900 dark:text-neutral-50 rounded-xl text-[13px] font-bold transition-colors")

with open('src/pages/settings/AutoComment.tsx', 'w') as f:
    f.write(content)

print("Fixed AutoComment!")
