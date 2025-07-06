from enum import Enum
from pydantic import BaseModel, Field


class Status(str, Enum):
    open = "open"
    closed = "closed"


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Ticket(BaseModel):
    id: int
    title: str = Field(..., alias="todo")
    status: Status
    priority: Priority
    assignee: str
    raw: dict  # puni JSON iz izvora
