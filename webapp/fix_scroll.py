with open('src/components/Layout.tsx', 'r') as f:
    content = f.read()

# Remove overflow-y-auto from main to let the body scroll naturally
content = content.replace('overflow-y-auto', '')

# Remove overflow-x-hidden from the main wrapper, just in case it breaks sticky
content = content.replace('overflow-x-hidden ', '')

with open('src/components/Layout.tsx', 'w') as f:
    f.write(content)

print("Fixed scrolling!")
