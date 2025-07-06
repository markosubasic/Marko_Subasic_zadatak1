# TicketHub – zadatak 1

Minimalni REST servis u FastAPI-ju koji dohvaća *support tickete* s DummyJSON-a.

## Pokretanje lokalno

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn tickethub.main:app --reload
