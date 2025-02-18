#TESTS FastAPI
from fastapi.testclient import TestClient


from main import app
client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


def test_get_users():
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyIiwiZXhwIjoxNzM5OTE4MzI4fQ.3XFKEde6MV05mgaDlcyImZJtYU7su_vd6CKwGyM7ZL8"} 
    response = client.get("/users/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["username"] == "user"

def test_create_user():
    response = client.post(
        "/register/",
        json={"username": "testuser", "email": "testuser@example.com", "full_name": "Test User", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"  

# Тест на повторную регистрацию с тем же username/email
def test_duplicate_registration():
    response = client.post(
        "/register/",
        json={"username": "testingUser", "email": "testingUser@mail.ru",
    "full_name": "Testing User", "password": "password"},
    )
    assert response.status_code == 200

# Тест аутентификации
def test_login():
    response = client.post(
        "/token",
        data={"username": "testingUser", "password": "password"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

# Тест аутентификации с неверным паролем
def test_login_invalid_password():
    response = client.post(
        "/token",
        data={"username": "testingUser", "password": "password1"},
    )
    assert response.status_code == 401 

# Тест получения списка пользователей
def test_get_users():
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyIiwiZXhwIjoxNzM5OTE4MzI4fQ.3XFKEde6MV05mgaDlcyImZJtYU7su_vd6CKwGyM7ZL8"}
    response = client.get("/users/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

# Тест получения информации о текущем пользователе
def test_get_current_user():
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyIiwiZXhwIjoxNzM5OTE4MzI4fQ.3XFKEde6MV05mgaDlcyImZJtYU7su_vd6CKwGyM7ZL8"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "username" in data

# Тест удаления пользователя
def test_delete_user():
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyIiwiZXhwIjoxNzM5OTE4MzI4fQ.3XFKEde6MV05mgaDlcyImZJtYU7su_vd6CKwGyM7ZL8"}
    response = client.delete("/users/11", headers=headers)
    assert response.status_code == 200
    response = client.delete("/users/11", headers=headers)
    assert response.status_code == 404

# Тест обновления пользователя
def test_update_user():
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyIiwiZXhwIjoxNzM5OTE4MzI4fQ.3XFKEde6MV05mgaDlcyImZJtYU7su_vd6CKwGyM7ZL8"}
    response = client.put(
        "/users/3",
        headers=headers,
        json={"full_name": "newemail@mail.ru"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "newemail@mail.ru"


