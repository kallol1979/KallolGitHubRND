import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    test_email = "pytestuser@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/unregister?email={test_email}")
    resp_signup = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp_signup.status_code == 200
    assert f"Signed up {test_email}" in resp_signup.json().get("message", "")
    resp_unreg = client.post(f"/activities/{activity}/unregister?email={test_email}")
    assert resp_unreg.status_code == 200
    assert f"Removed {test_email}" in resp_unreg.json().get("message", "")
    resp_unreg2 = client.post(f"/activities/{activity}/unregister?email={test_email}")
    assert resp_unreg2.status_code == 404
    assert "Participant not found" in resp_unreg2.json().get("detail", "")
    resp_signup2 = client.post(f"/activities/Nonexistent/signup?email={test_email}")
    assert resp_signup2.status_code == 404
    assert "Activity not found" in resp_signup2.json().get("detail", "")
