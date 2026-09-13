with open('webapp/src/components/ui.tsx', 'r') as f:
    text = f.read()

text = text.replace("import { X, Lock }", "import { X, Lock, Info }")

with open('webapp/src/components/ui.tsx', 'w') as f:
    f.write(text)
