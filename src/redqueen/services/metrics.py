"""Prometheus-compatible metrics collector for RedQueen."""
import time
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST

_start_time = time.time()

# Define prometheus metrics
MESSAGES_PROCESSED = Counter('redqueen_messages_processed_total', 'Total processed messages')
AI_VERDICTS = Counter('redqueen_ai_verdicts_total', 'Total AI verdicts')
AI_VERDICTS_SPAM = Counter('redqueen_ai_verdicts_spam', 'Total AI verdicts spam')
AI_VERDICTS_SAFE = Counter('redqueen_ai_verdicts_safe', 'Total AI verdicts safe')
MODERATION_ACTIONS = Counter('redqueen_moderation_actions_total', 'Total moderation actions')
CAPTCHA_CHALLENGES = Counter('redqueen_captcha_challenges_total', 'Total captcha challenges')
CAPTCHA_PASSED = Counter('redqueen_captcha_passed_total', 'Total captcha passed')
CAPTCHA_FAILED = Counter('redqueen_captcha_failed_total', 'Total captcha failed')
RAID_EVENTS = Counter('redqueen_raid_events_total', 'Total raid events')
PAYMENTS = Counter('redqueen_payments_total', 'Total payments')
API_REQUESTS = Counter('redqueen_api_requests_total', 'Total api requests')
API_ERRORS = Counter('redqueen_api_errors_total', 'Total api errors')

ACTIVE_CHATS = Gauge('redqueen_active_chats', 'Active chats')
ACTIVE_SUBSCRIPTIONS = Gauge('redqueen_active_subscriptions', 'Active subscriptions')
AI_LATENCY = Gauge('redqueen_ai_latency_seconds', 'AI latency seconds')
UPTIME = Gauge('redqueen_uptime_seconds', 'Bot uptime in seconds')

_counter_map = {
    "messages_processed_total": MESSAGES_PROCESSED,
    "ai_verdicts_total": AI_VERDICTS,
    "ai_verdicts_spam": AI_VERDICTS_SPAM,
    "ai_verdicts_safe": AI_VERDICTS_SAFE,
    "moderation_actions_total": MODERATION_ACTIONS,
    "captcha_challenges_total": CAPTCHA_CHALLENGES,
    "captcha_passed_total": CAPTCHA_PASSED,
    "captcha_failed_total": CAPTCHA_FAILED,
    "raid_events_total": RAID_EVENTS,
    "payments_total": PAYMENTS,
    "api_requests_total": API_REQUESTS,
    "api_errors_total": API_ERRORS,
}

_gauge_map = {
    "active_chats": ACTIVE_CHATS,
    "active_subscriptions": ACTIVE_SUBSCRIPTIONS,
    "ai_latency_seconds": AI_LATENCY,
}


def inc(name: str, amount: int = 1) -> None:
    """Increment a counter."""
    if name in _counter_map:
        _counter_map[name].inc(amount)


def set_gauge(name: str, value: float) -> None:
    """Set a gauge value."""
    if name in _gauge_map:
        _gauge_map[name].set(value)


async def collect_metrics(app=None) -> bytes:
    """Render Prometheus text format."""
    uptime = time.time() - _start_time
    UPTIME.set(uptime)
    return generate_latest()
