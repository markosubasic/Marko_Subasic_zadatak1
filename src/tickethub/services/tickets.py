
from __future__ import annotations

import asyncio
from collections.abc import Sequence
from typing import Final

from tickethub.clients.dummyjson import fetch_todos, fetch_users
from tickethub.models import Ticket, Status, Priority

_MAX_DESC: Final[int] = 100


def _truncate(text: str, length: int = _MAX_DESC) -> str:
    return text if len(text) <= length else text[: length - 3] + "..."


try:
    from tickethub.core.cache import cache  
except ModuleNotFoundError:  
    cache = None  

def _build_ticket(todo: dict, users: dict[int, str]) -> Ticket:
    pri = ["low", "medium", "high"][todo["id"] % 3]

    return Ticket(
        id=todo["id"],
        title=todo["todo"],  
        status=Status.closed if todo["completed"] else Status.open,
        priority=Priority(pri),
        assignee=users.get(todo["userId"], "unknown"),
        description=_truncate(todo["todo"]),
        raw=todo,
    )

async def load_tickets() -> list[Ticket]:
    if cache:
        cached = await cache.get("tickets")
        if cached:
            return [Ticket(**t) for t in cached]

    todos, users = await asyncio.gather(fetch_todos(), fetch_users())
    tickets = [_build_ticket(t, users) for t in todos]

    if cache:
        await cache.set("tickets", [t.model_dump() for t in tickets])

    return tickets


def filter_tickets(
    tickets: Sequence[Ticket],
    status: Status | None = None,
    priority: Priority | None = None,
) -> list[Ticket]:
    out = tickets
    if status:
        out = [t for t in out if t.status == status]
    if priority:
        out = [t for t in out if t.priority == priority]
    return list(out)
