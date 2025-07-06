run:
	uvicorn tickethub.main:app --reload

test:
	pytest -q

lint:
	ruff check src tests

run:
	uvicorn --app-dir src tickethub.main:app --reload
