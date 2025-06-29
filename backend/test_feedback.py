from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def get_token():
    res = client.post("/token", data={"username": "alice", "password": "secret"})
    assert res.status_code == 200
    return res.json()["access_token"]

def test_feedback_success(monkeypatch):
    from dynamo_client import log_event
    monkeypatch.setattr("dynamo_client.log_event", lambda u, t, m: None)
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"feedback": 1, "variant": "A", "prompt": "Write a welcome message"}
    res = client.post("/feedback", json=payload, headers=headers)
    assert res.status_code == 200
    assert res.json()["status"] == "success"

def test_feedback_invalid(monkeypatch):
    from dynamo_client import log_event
    monkeypatch.setattr("dynamo_client.log_event", lambda u, t, m: None)
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"feedback": 3, "variant": "A"}
    res = client.post("/feedback", json=payload, headers=headers)
    assert res.status_code == 400

def test_feedback_unauthorized():
    payload = {"feedback": 1, "variant": "A"}
    res = client.post("/feedback", json=payload)
    assert res.status_code == 401