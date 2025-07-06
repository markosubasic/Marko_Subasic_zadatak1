from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from tickethub.core.config import get_settings
from tickethub.core.logging import configure_logging
from tickethub.routers import tickets, auth, stats

configure_logging()

settings = get_settings()
limiter = Limiter(key_func=lambda request: request.client.host, default_limits=[settings.rate_limit])

app = FastAPI(title="TicketHub", version="0.2.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(auth.router)
app.include_router(tickets.router)
app.include_router(stats.router)

@app.get("/", include_in_schema=False)
async def index():
    return {
        "message": "TicketHub API",
        "docs": "/docs",
        "tickets": "/tickets",
        "health": "/healthz",
    }

@app.get("/healthz", tags=["infra"])
async def health():
    return {"status": "ok"}
