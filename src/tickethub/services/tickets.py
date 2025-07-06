import asyncio
from collections.abc import Sequence
from tickethub.clients.dummyjson import fetch_todos, fetch_users
from tickethub.models import Ticket, Status, Priority


async def _build_ticket(todo: dict, users: dict[int, str]) -> Ticket:
    pri = ["low", "medium", "high"][todo["id"] % 3]
    return Ticket(
        id=todo["id"],
        todo=todo["todo"],
        status=Status.closed if todo["completed"] else Status.open,
        priority=Priority(pri),
        assignee=users.get(todo["userId"], "unknown"),
        raw=todo,
    )


async def load_tickets() -> list[Ticket]:
    todos, users = await asyncio.gather(fetch_todos(), fetch_users())
    return [await _build_ticket(t, users) for t in todos]


def filter_tickets(
    tickets: Sequence[Ticket],
    status: Status | None,
    priority: Priority | None,
) -> list[Ticket]:
    out = tickets
    if status:
        out = [t for t in out if t.status == status]
    if priority:
        out = [t for t in out if t.priority == priority]
    return list(out)
