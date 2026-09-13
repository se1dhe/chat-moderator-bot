import re

with open('src/redqueen/handlers/ai_review.py', 'r') as f:
    text = f.read()

print("get_chat_moderators" in text)
