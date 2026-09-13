with open('src/pages/settings/RBAC.tsx', 'r') as f:
    content = f.read()

# Fix API endpoints
content = content.replace("api.get(`/api/chats/", "api.get(`/chats/")
content = content.replace("api.post(`/api/chats/", "api.post(`/chats/")
content = content.replace("api.delete(`/api/chats/", "api.del(`/chats/")

with open('src/pages/settings/RBAC.tsx', 'w') as f:
    f.write(content)

print("Fixed API calls in RBAC!")
