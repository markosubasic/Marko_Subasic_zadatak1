from pydantic import BaseModel
from enum import Enum


class Status(str, Enum):
    open = "open"
    closed = "closed"


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Ticket(BaseModel):
    id: int
    title: str
    status: Status
    priority: Priority
    assignee: str
    description: str           
    raw: dict
