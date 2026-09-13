with open('src/pages/Members.tsx', 'r') as f:
    content = f.read()

content = content.replace("              </div>\n            );\n          })\n        )}", "              </motion.div>\n            );\n          })\n        )}")

with open('src/pages/Members.tsx', 'w') as f:
    f.write(content)
