import re

with open('src/pages/Triggers.tsx', 'r') as f:
    content = f.read()

# Replace the giant button classes
# w-full flex items-center justify-center gap-2 py-3 bg-red-500 hover:bg-red-600 text-white rounded-xl font-bold transition-all active:scale-95 shadow-md shadow-red-500/20 text-[15px] px-3 py-1 text-[13px]
content = re.sub(
    r'className="w-full flex items-center justify-center gap-2 py-3 bg-red-500 hover:bg-red-600 text-white rounded-xl font-bold transition-all active:scale-95 shadow-md shadow-red-500/20 text-\[15px\] px-3 py-1 text-\[13px\]"',
    'className="shrink-0 flex items-center justify-center gap-1.5 px-3 py-1.5 bg-red-500/10 hover:bg-red-500/20 text-red-500 rounded-lg font-bold transition-all active:scale-95 text-[13px]"',
    content
)

# And fix the duplicate margin classes "ml-1 mt-4 mb-2 mt-6"
content = content.replace("ml-1 mt-4 mb-2 mt-6", "ml-1 mt-6 mb-2")

# And fix any leftover /60/50
content = content.replace("border-neutral-800/60/50", "border-neutral-800/60")

with open('src/pages/Triggers.tsx', 'w') as f:
    f.write(content)

print("Fixed Triggers!")
