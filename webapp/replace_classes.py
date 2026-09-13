import os
import glob

def replace_in_file(path):
    with open(path, 'r') as f:
        content = f.read()

    # Cards
    content = content.replace('className="card"', 'className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-2xl p-2 mb-4 shadow-sm w-full"')
    content = content.replace('className="card card-pad"', 'className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-2xl p-4 mb-4 shadow-sm w-full"')
    
    # Section Labels
    content = content.replace('className="section-label"', 'className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2"')
    
    # Buttons
    content = content.replace('className="btn btn-primary"', 'className="w-full flex items-center justify-center gap-2 py-3 bg-primary hover:bg-primary-dark text-white rounded-xl font-bold transition-all active:scale-95 shadow-md shadow-primary/20 text-[15px]"')
    content = content.replace('className="btn btn-danger"', 'className="w-full flex items-center justify-center gap-2 py-3 bg-red-500 hover:bg-red-600 text-white rounded-xl font-bold transition-all active:scale-95 shadow-md shadow-red-500/20 text-[15px]"')
    content = content.replace('className="btn btn-secondary"', 'className="w-full flex items-center justify-center gap-2 py-3 bg-neutral-200 dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 rounded-xl font-bold transition-all active:scale-95 border border-neutral-300 dark:border-neutral-700 text-[15px]"')
    content = content.replace('className="btn"', 'className="w-full flex items-center justify-center gap-2 py-3 bg-neutral-200 dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 rounded-xl font-bold transition-all active:scale-95 text-[15px]"')
    
    # Inputs
    content = content.replace('className="input"', 'className="w-full px-4 py-3 bg-neutral-50 dark:bg-neutral-950 border border-neutral-200 dark:border-neutral-800 rounded-xl focus:outline-none focus:border-primary/50 transition-colors font-medium text-[15px]"')
    content = content.replace('className="input member-reason"', 'className="w-full px-3 py-2 bg-neutral-50 dark:bg-neutral-950 border border-neutral-200 dark:border-neutral-800 rounded-lg text-[13px] focus:outline-none focus:border-primary/50 transition-colors mt-2 mb-2"')

    with open(path, 'w') as f:
        f.write(content)

files = glob.glob('src/pages/settings/*.tsx') + ['src/pages/Triggers.tsx']
for file in files:
    replace_in_file(file)

print("Done")
