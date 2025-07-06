from fastapi import APIRouter, Query, HTTPException
from tickethub.models import Status, Priority
from tickethub.services.tickets import load_tickets, filter_tickets

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.get("", summary="Lista ticketa")
async def list_tickets(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    status: Status | None = None,
    priority: Priority | None = None,
):
    tickets = filter_tickets(await load_tickets(), status, priority)
    start = (page - 1) * size
    page_items = tickets[start : start + size]
    return {
        "items": [t.model_dump(by_alias=False) for t in page_items],
        "total": len(tickets),
        "page": page,
        "size": size,
    }

@router.get("/search", summary="Pretraga po nazivu")
async def search_tickets(q: str):
    tickets = await load_tickets()
    return [
        t.model_dump(by_alias=False)
        for t in tickets
        if q.lower() in t.title.lower()
    ]


@router.get("/{ticket_id}", summary="Detalj ticketa")
async def ticket_detail(ticket_id: int):
    for t in await load_tickets():
        if t.id == ticket_id:
            return {
                "ticket": t.model_dump(by_alias=False),
                "raw": t.raw,
            }
    raise HTTPException(404, "Ticket not found")
