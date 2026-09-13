import re

with open('src/pages/Quarantine.tsx', 'r') as f:
    content = f.read()

if 'import { motion, AnimatePresence } from' not in content:
    content = content.replace("import { ShieldCheck", "import { motion, AnimatePresence } from 'framer-motion';\nimport { ShieldCheck")
    
    # Wrap items.map in AnimatePresence
    content = content.replace('{items.map((v) => (', '<AnimatePresence>\n        {items.map((v) => (')
    content = content.replace('))}</div>', '))}\n        </AnimatePresence>\n      </div>')
    
    # Change div to motion.div inside map
    content = content.replace('<div key={v.id} className="p-4 bg-white dark:bg-[#0a0a0a]', 
                              '<motion.div key={v.id} initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.9, height: 0 }} className="p-4 bg-white dark:bg-[#0a0a0a]')
    
    content = content.replace('</button>\n            </div>\n          </div>', '</button>\n            </div>\n          </motion.div>')

    with open('src/pages/Quarantine.tsx', 'w') as f:
        f.write(content)
    print("Patched Quarantine")
