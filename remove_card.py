import re

with open('src/redqueen/handlers/ai_review.py', 'r') as f:
    text = f.read()

card_start = text.find('card = t(')
card_end = text.find(')', card_start + 10) + 1

if card_start != -1 and card_end != -1:
    new_text = text[:card_start] + text[card_end:]
    with open('src/redqueen/handlers/ai_review.py', 'w') as f:
        f.write(new_text)
