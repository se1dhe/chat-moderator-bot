"""Prometheus-compatible metrics collector for RedQueen."""
import time

_start_time = time.time()

# Simple counters — in-memory for now
_counters: dict[str, int] = {
    "messages_processed_total": 0,
    "ai_verdicts_total": 0,
    "ai_verdicts_spam": 0,
    "ai_verdicts_safe": 0,
    "moderation_actions_total": 0,
    "captcha_challenges_total": 0,
    "captcha_passed_total": 0,
    "captcha_failed_total": 0,
    "raid_events_total": 0,
    "payments_total": 0,
    "api_requests_total": 0,
    "api_errors_total": 0,
}

_gauges: dict[str, float] = {
    "active_chats": 0,
    "active_subscriptions": 0,
    "ai_latency_seconds": 0.0,
}


def inc(name: str, amount: int = 1) -> None:
    """Increment a counter."""
    if name in _counters:
        _counters[name] += amount


def set_gauge(name: str, value: float) -> None:
    """Set a gauge value."""
    _gauges[name] = value


async def collect_metrics(app=None) -> str:
    """Render Prometheus text format."""
    lines = []
    uptime = time.time() - _start_time
    lines.append("# HELP redqueen_uptime_seconds Bot uptime in seconds")
    lines.append("# TYPE redqueen_uptime_seconds gauge")
    lines.append(f"redqueen_uptime_seconds {uptime:.1f}")
    lines.append("")
    
    for name, val in _counters.items():
        lines.append(f"# TYPE redqueen_{name} counter")
        lines.append(f"redqueen_{name} {val}")
    lines.append("")
    
    for name, val in _gauges.items():
        lines.append(f"# TYPE redqueen_{name} gauge")
        lines.append(f"redqueen_{name} {val}")
    
    return "\n".join(lines) + "\n"
