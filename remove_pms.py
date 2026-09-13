import re

with open('src/redqueen/handlers/ai_review.py', 'r') as f:
    text = f.read()

# I will find _notify_admins and delete it, and the asyncio.create_task(_notify_admins())
start_idx = text.find('async def _notify_admins():')
end_idx = text.find('asyncio.create_task(_notify_admins())') + len('asyncio.create_task(_notify_admins())')

if start_idx != -1 and end_idx != -1:
    new_text = text[:start_idx] + text[end_idx:]
    # Now remove markup and card generation as it's not needed anymore
    new_text = new_text.replace('markup = _decision_kb(row.id, t).as_markup()', '')
    
    with open('src/redqueen/handlers/ai_review.py', 'w') as f:
        f.write(new_text)
