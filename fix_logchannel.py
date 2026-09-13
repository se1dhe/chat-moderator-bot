with open('src/redqueen/services/config.py', 'r') as f:
    text = f.read()

# Add to default config
text = text.replace('"onboarding": {', '"log_channel_id": None,\n    "onboarding": {')

# Add to export
text = text.replace('"onboarding": cfg["onboarding"],', '"log_channel_id": cfg.get("log_channel_id"),\n        "onboarding": cfg["onboarding"],')

# Add to patch
new_patch = """
    if "log_channel_id" in patch:
        val = patch["log_channel_id"]
        cfg["log_channel_id"] = int(val) if val else None

    if "onboarding" in patch:"""
text = text.replace('    if "onboarding" in patch:', new_patch)

with open('src/redqueen/services/config.py', 'w') as f:
    f.write(text)

