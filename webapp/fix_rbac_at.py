with open('src/pages/settings/RBAC.tsx', 'r') as f:
    content = f.read()

# Remove the absolute @ wrapper and adjust input padding
content = content.replace("""          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
            <span className="text-neutral-400 font-medium">@</span>
          </div>
          <input 
            className="w-full pl-8 pr-4 py-3""", """          <input 
            className="w-full px-4 py-3""")

with open('src/pages/settings/RBAC.tsx', 'w') as f:
    f.write(content)

print("Fixed double @!")
