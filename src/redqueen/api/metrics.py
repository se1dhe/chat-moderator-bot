from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from aiohttp import web

# Define basic metrics
MESSAGES_PROCESSED = Counter('redqueen_messages_processed_total', 'Total processed messages')
COMMANDS_EXECUTED = Counter('redqueen_commands_executed_total', 'Total commands executed')
BANS_ISSUED = Counter('redqueen_bans_issued_total', 'Total bans issued')
API_REQUEST_DURATION = Histogram('redqueen_api_request_duration_seconds', 'API Request Duration')

async def metrics_handler(request: web.Request) -> web.Response:
    """Prometheus metrics endpoint."""
    data = generate_latest()
    return web.Response(body=data, content_type=CONTENT_TYPE_LATEST)
