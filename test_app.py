# test_app.py

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Mission: Identity Fusion Scenario
def test_d1n_fusion_1():
    payload = {"email": "doc1@zamazon.com", "phoneNumber": "1112223333"}
    res = client.post("/identify", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "primaryContactId" in data
    assert "emails" in data and "phoneNumbers" in data
    assert isinstance(data["emails"], list)
    assert isinstance(data["secondaryContactIds"], list)

# Fusion with new phone
def test_d1n_fusion_2():
    payload = {"email": "doc1@zamazon.com", "phoneNumber": "4445556666"}
    res = client.post("/identify", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert len(data["phoneNumbers"]) >= 2
    assert len(data["secondaryContactIds"]) >= 1

# Defensive Cloaking - empty request
def test_cloaking_error():
    payload = {}
    res = client.post("/identify", json=payload)
    assert res.status_code == 418
