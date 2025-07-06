# TicketHub – zadatak 1

Minimalni REST servis u FastAPI-ju koji dohvaća *support tickete* s DummyJSON-a.

## Pokretanje lokalno

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn tickethub.main:app --reload

Redis caching – pokreni docker compose up; aplikacija automatski čita varijablu REDIS_URL.

Rate-limiting – postavi varijablu RATE_LIMIT (npr. RATE_LIMIT=60/minute, podrazumijevana vrijednost).

JWT autentifikacija – POST /auth/login s DummyJSON korisničkim imenom i lozinkom; odgovor sadrži Bearer token.

Statistike – GET /stats uz HTTP header Authorization: Bearer <token> (potreban token dobiven loginom)