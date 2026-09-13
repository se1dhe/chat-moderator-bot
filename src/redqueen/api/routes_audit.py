from aiohttp import web
import csv
import io
from datetime import datetime, timedelta, timezone

from ..db import repo
from .auth import require_chat_admin
from .utils import _chat_id, _session
from sqlalchemy import select
from ..db.models import ModAction

async def audit_export(request: web.Request) -> web.Response:
    cid = _chat_id(request)
    await require_chat_admin(request, cid)
    
    since = datetime.now(timezone.utc) - timedelta(days=30)
    
    async with _session(request) as session:
        # Get actions for the last 30 days
        result = await session.execute(
            select(ModAction)
            .where(ModAction.chat_telegram_id == cid, ModAction.created_at >= since)
            .order_by(ModAction.id.desc())
        )
        actions = result.scalars().all()
        
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Action", "User ID", "Actor ID", "Reason", "Created At"])
    
    for action in actions:
        writer.writerow([
            action.id,
            action.action,
            action.user_telegram_id,
            action.actor_id,
            action.reason or "",
            action.created_at.isoformat() if action.created_at else ""
        ])
        
    csv_data = output.getvalue()
    
    return web.Response(
        body=csv_data,
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="audit.csv"'}
    )
