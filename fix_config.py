import re

with open('src/redqueen/services/config.py', 'r') as f:
    text = f.read()

# Replace default config for raid with defcon
old_cfg = """    "raid": {
        "enabled": False,
        "join_threshold": 5,
        "window_seconds": 30,
        "lock_seconds": 600,
        "locked_until": None,  # epoch seconds, or None when not locked
    },"""
new_cfg = """    "defcon": {
        "enabled": False,
        "threshold": 10,
        "action": "read_only",  # read_only, strict, captcha
        "lock_seconds": 900,
        "active_until": None,
    },"""
text = text.replace(old_cfg, new_cfg)

old_export = """        "raid": {k: v for k, v in cfg["raid"].items() if k != "locked_until"}
        | {"locked": bool(cfg["raid"].get("locked_until"))},"""
new_export = """        "defcon": {k: v for k, v in cfg["defcon"].items() if k != "active_until"}
        | {"active": bool(cfg["defcon"].get("active_until"))},"""
text = text.replace(old_export, new_export)

old_patch = """    if "raid" in patch:
        r, cur = patch["raid"], cfg["raid"]
        cfg["raid"] = {
            **cur,
            "enabled": _as_bool(r.get("enabled"), cur["enabled"]),
            "join_threshold": _clamp(r.get("join_threshold"), 2, 100, cur["join_threshold"]),
            "window_seconds": _clamp(r.get("window_seconds"), 5, 600, cur["window_seconds"]),
            "lock_seconds": _clamp(r.get("lock_seconds"), 60, 86400, cur["lock_seconds"]),
        }
        # The Mini App may only *clear* an active lock, never set one.
        if r.get("locked") is False:
            cfg["raid"]["locked_until"] = None"""
new_patch = """    if "defcon" in patch:
        r, cur = patch["defcon"], cfg["defcon"]
        cfg["defcon"] = {
            **cur,
            "enabled": _as_bool(r.get("enabled"), cur["enabled"]),
            "threshold": _clamp(r.get("threshold"), 2, 100, cur["threshold"]),
            "action": str(r.get("action", cur["action"])),
            "lock_seconds": _clamp(r.get("lock_seconds"), 60, 86400, cur["lock_seconds"]),
        }
        if r.get("active") is False:
            cfg["defcon"]["active_until"] = None"""
text = text.replace(old_patch, new_patch)

with open('src/redqueen/services/config.py', 'w') as f:
    f.write(text)

