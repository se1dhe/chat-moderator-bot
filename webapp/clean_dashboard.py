with open('src/pages/Dashboard.tsx', 'r') as f:
    text = f.read()

# Strip out the mistakenly injected variants inside the map
import re
text = re.sub(r'  const container = \{.*?mass: 0.5 \} \}\n  \};\n\n  return \(\n', '              return (\n', text, flags=re.DOTALL)

# Now inject it before the FIRST return (
variants = """
  const container = {
    hidden: { opacity: 0 },
    show: { opacity: 1, transition: { staggerChildren: 0.03 } }
  };
  const item = {
    hidden: { opacity: 0, y: 8, scale: 0.97 },
    show: { opacity: 1, y: 0, scale: 1, transition: { type: "spring", stiffness: 500, damping: 30, mass: 0.5 } }
  };

  return (
"""

text = text.replace('  return (\n    <motion.div variants={container}', variants + '    <motion.div variants={container}')

with open('src/pages/Dashboard.tsx', 'w') as f:
    f.write(text)
