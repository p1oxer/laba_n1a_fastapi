from fastapi.testclient import TestClient


from main import app
client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


def test_get_users():
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6MTczOTk1MzUwN30.mQGbRg4KPj7oxndhPUxJd1-HpzwgyGnDvLcYwtR8KVc"} 
    response = client.get("/users/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["username"] == "user"

def test_create_user():
    response = client.post(
        "/register/",
        json={"username": "newuser", "email": "newuser@example.com", "full_name": "Test User", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com" 