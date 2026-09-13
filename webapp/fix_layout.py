import re

with open('src/components/Layout.tsx', 'r') as f:
    content = f.read()

# Replace the {outlet} with a frozen context or just remove AnimatePresence for the main layout to avoid bugs
# The best way to avoid all react-router AnimatePresence bugs is to just use standard tailwind animations or a frozen outlet.
# Let's freeze the outlet.
# Wait, actually, removing AnimatePresence and motion.div from the router outlet is much safer and cleaner since the individual pages already have `animate-in`!

old_animate = """          <AnimatePresence mode="wait">
            <motion.div
              key={location.pathname}
              initial={{ opacity: 0, scale: 0.98, y: 10 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.98, y: -10 }}
              transition={{ duration: 0.25, ease: "easeOut" }}
              className="flex-1 flex flex-col w-full min-h-0"
            >
              {outlet}
            </motion.div>
          </AnimatePresence>"""

new_animate = "          {outlet}"

if old_animate in content:
    content = content.replace(old_animate, new_animate)
else:
    # try regex
    content = re.sub(r'<AnimatePresence mode="wait">[\s\S]*?</AnimatePresence>', '{outlet}', content)

with open('src/components/Layout.tsx', 'w') as f:
    f.write(content)

print("Fixed layout router animation!")
