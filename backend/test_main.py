from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login_and_generate():
    res = client.post("/token", data={"username": "alice", "password": "secret"})
    assert res.status_code == 200
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    res = client.post("/generate", json={"prompt": "Write a welcome message"}, headers=headers)
    assert res.status_code == 200
    assert "content" in res.json()

def test_unauthorized_generate():
    res = client.post("/generate", json={"prompt": "Unauthorized access"})
    assert res.status_code == 401