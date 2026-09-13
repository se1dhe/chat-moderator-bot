with open('src/components/Layout.tsx', 'r') as f:
    content = f.read()

# Make the title hidden on small screens if in Telegram, to give space to toggles
content = content.replace(
    "<h1 className=\"text-lg font-bold truncate text-neutral-900 dark:text-white tracking-tight dark:drop-shadow-[0_2px_10px_rgba(0,0,0,1)]\">",
    "<h1 className={`text-lg font-bold truncate text-neutral-900 dark:text-white tracking-tight dark:drop-shadow-[0_2px_10px_rgba(0,0,0,1)] ${isTelegram ? 'hidden sm:block' : ''}`}>"
)

with open('src/components/Layout.tsx', 'w') as f:
    f.write(content)

print("Fixed header title!")
