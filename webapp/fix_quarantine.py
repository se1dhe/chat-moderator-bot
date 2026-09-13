with open('src/pages/Quarantine.tsx', 'r') as f:
    content = f.read()

content = content.replace("import { ShieldCheck", "import { motion, AnimatePresence } from 'framer-motion';\nimport { ShieldCheck")

content = content.replace("{items.map((v) => (", "<AnimatePresence>\n        {items.map((v) => (")

content = content.replace('<div key={v.id} className="p-4 bg-white', '<motion.div key={v.id} layout initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.9, height: 0 }} className="p-4 bg-white')

content = content.replace("          </div>\n        ))}\n      </div>\n    </div>", "          </motion.div>\n        ))}\n        </AnimatePresence>\n      </div>\n    </div>")

with open('src/pages/Quarantine.tsx', 'w') as f:
    f.write(content)
