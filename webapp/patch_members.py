with open('src/pages/Members.tsx', 'r') as f:
    content = f.read()

content = content.replace("import { Users", "import { motion, AnimatePresence } from 'framer-motion';\nimport { Users")

# 1. wrap rows.map in AnimatePresence
content = content.replace("        ) : (\n          rows.map((m) => {", "        ) : (\n          <AnimatePresence>\n          {rows.map((m) => {")
# 2. replace </div> with </motion.div> for the item
content = content.replace("              <div key={m.user_id} className=\"bg-white", "              <motion.div layout initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.9, height: 0 }} key={m.user_id} className=\"bg-white")
content = content.replace("              </div>\n            );\n          })\n        )}", "              </motion.div>\n            );\n          })}\n          </AnimatePresence>\n        )}", 1)

with open('src/pages/Members.tsx', 'w') as f:
    f.write(content)
