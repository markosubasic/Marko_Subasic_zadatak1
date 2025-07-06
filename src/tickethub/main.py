from fastapi import FastAPI
from tickethub.routers.tickets import router as tickets_router

app = FastAPI(title="TicketHub", version="0.1.0")

app.include_router(tickets_router)

@app.get("/", include_in_schema=False)
async def index():
    return {
        "message": "Welcome to TicketHub API",
        "docs": "/docs",
        "tickets": "/tickets"
    }
@app.get("/healthz", tags=["infra"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
