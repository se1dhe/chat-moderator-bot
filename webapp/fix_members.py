with open('src/pages/Members.tsx', 'r') as f:
    content = f.read()

content = content.replace("import { Users", "import { motion, AnimatePresence } from 'framer-motion';\nimport { Users")

content = content.replace("{members.map((m) => {", "<AnimatePresence>\n        {members.map((m) => {")

content = content.replace("          <div key={m.user_id} className=\"p-4 bg-white", "          <motion.div key={m.user_id} layout initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.9, height: 0 }} className=\"p-4 bg-white")

content = content.replace("              </div>\n            );\n          })\n        )}", "              </motion.div>\n            );\n          })\n        )}\n      </AnimatePresence>")

with open('src/pages/Members.tsx', 'w') as f:
    f.write(content)
