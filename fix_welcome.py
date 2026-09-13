import sys

filename = "src/redqueen/handlers/welcome.py"
with open(filename, "r") as f:
    text = f.read()

# Fix the config path access
text = text.replace('use_global_bans = data.get("use_global_bans", False)', 'use_global_bans = data.get("modes", {}).get("use_global_bans", False)')
text = text.replace('welcome_message = data.get("welcome_message", "")', 'welcome_message = data.get("onboarding", {}).get("welcome_message", "")')

# Make sure the function ends with raise SkipHandler
if "raise SkipHandler" not in text.split("def on_user_join")[-1]:
    # I'll just append it to the file but inside the function is better
    pass # Wait, let's just rewrite welcome.py

