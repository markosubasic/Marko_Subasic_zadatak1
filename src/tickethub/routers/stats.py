from collections import Counter
from fastapi import APIRouter, Depends
from tickethub.services.tickets import load_tickets
from tickethub.core.security import get_current_user

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("", dependencies=[Depends(get_current_user)])
async def stats():
    tickets = await load_tickets()
    by_status = Counter(t.status for t in tickets)
    by_priority = Counter(t.priority for t in tickets)
    return {"total": len(tickets), "status": dict(by_status), "priority": dict(by_priority)}
