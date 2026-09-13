import os
import re

def replace_in_file(filepath, replacements):
    if not os.path.exists(filepath): return
    with open(filepath, 'r') as f:
        content = f.read()
    
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    with open(filepath, 'w') as f:
        f.write(content)

# We will apply a set of premium styles to specific known strings
replacements = {
    # Update main backgrounds to be slightly darker and richer
    'bg-neutral-50 dark:bg-neutral-950': 'bg-neutral-50 dark:bg-black',
    'bg-white dark:bg-neutral-900': 'bg-white dark:bg-[#0a0a0a]',
    
    # Premium borders
    'border-neutral-200 dark:border-neutral-800': 'border-neutral-200 dark:border-neutral-800/60',
    
    # Text headers
    'text-lg font-bold truncate text-neutral-900 dark:text-neutral-50 tracking-tight leading-tight': 'text-lg font-bold truncate text-neutral-900 dark:text-white tracking-tight leading-tight dark:drop-shadow-[0_2px_10px_rgba(0,0,0,1)]',
    'text-lg font-bold truncate text-neutral-900 dark:text-neutral-50 tracking-tight': 'text-lg font-bold truncate text-neutral-900 dark:text-white tracking-tight dark:drop-shadow-[0_2px_10px_rgba(0,0,0,1)]',
    
    # Buttons
    'bg-primary hover:bg-primary-dark text-white': 'bg-gradient-to-r from-red-600 to-red-500 hover:from-red-500 hover:to-red-400 text-white shadow-[0_4px_20px_-4px_rgba(220,38,38,0.5)]',
    'shadow-md shadow-primary/20': '', # remove old shadows
    
    # Navigation styling
    'bg-white/80 dark:bg-neutral-900/80 backdrop-blur-md': 'bg-white/80 dark:bg-black/70 backdrop-blur-xl',
    'bg-white/90 dark:bg-neutral-900/90 backdrop-blur-lg': 'bg-white/90 dark:bg-black/80 backdrop-blur-2xl',
    
    # Glows around icons
    'text-primary shrink-0': 'text-primary shrink-0 drop-shadow-[0_0_8px_rgba(220,38,38,0.5)]',
}

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.tsx'):
            replace_in_file(os.path.join(root, file), replacements)

print("Applied premium styles!")
