import respx
from httpx import Response
from fastapi.testclient import TestClient

from tickethub.main import app

client = TestClient(app)

DUMMY_TODO = {
    "id": 1,
    "todo": "Write unit tests",
    "completed": False,
    "userId": 7,
}
DUMMY_USER = {"id": 7, "username": "alice"}


@respx.mock
def test_list_tickets():
    respx.get("https://dummyjson.com/todos").mock(
        return_value=Response(200, json={"todos": [DUMMY_TODO]})
    )
    respx.get("https://dummyjson.com/users").mock(
        return_value=Response(200, json={"users": [DUMMY_USER]})
    )
    resp = client.get("/tickets")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == DUMMY_TODO["todo"]
