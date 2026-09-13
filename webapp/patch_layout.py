import re

with open('src/components/Layout.tsx', 'r') as f:
    content = f.read()

# Replace the inner NavLink content
old_code = """          >
            <it.icon size={22} className={({ isActive }: any) => isActive ? 'fill-primary/10' : ''} />
            <span className="text-[10px] font-medium leading-none">{it.label}</span>
          </NavLink>"""

new_code = """          >
            {({ isActive }) => (
              <>
                <it.icon size={22} className={isActive ? 'fill-primary/10' : ''} />
                <span className="text-[10px] font-medium leading-none">{it.label}</span>
              </>
            )}
          </NavLink>"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open('src/components/Layout.tsx', 'w') as f:
        f.write(content)
    print("Patched Layout.tsx")
else:
    print("Could not find the exact code block.")

