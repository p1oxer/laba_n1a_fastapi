#TESTS FastAPI
from fastapi.testclient import TestClient

from main import app
client = TestClient(app)



access = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyIiwiZXhwIjoxNzM5OTU0NzQ3fQ.dUoOlzrykxK3WPCwBQuDsfc6QZmq6BMGfNptFlLo2wg"

def test_create_user():
    response = client.post(
        "/register/",
        json={"username": "testingUser321", "email": "testingUser321@mail.ru", "full_name": "Test User", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testingUser321"
    assert data["email"] == "testingUser321@mail.ru"  

# Тест на повторную регистрацию с тем же username/email
def test_duplicate_registration1():
    response = client.post(
        "/register/",
        json={"username": "testingUser123", "email": "testingUser123@mail.ru",
    "full_name": "Testing User", "password": "password"},
    )
    assert response.status_code == 200

def test_duplicate_registration():
    response = client.post(
        "/register/",
        json={"username": "testingUser123", "email": "testingUser123@mail.ru",
    "full_name": "Testing User", "password": "password"},
    )
    assert response.status_code == 401

# Тест аутентификации
def test_login():
    response = client.post(
        "/token",
        data={"username": "user", "password": "pass"},
    )
    assert response.status_code == 200
    data = response.json()
    print(data)
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
    headers = {"Authorization": f'Bearer {access}'}
    response = client.get("/users/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

# Тест получения информации о текущем пользователе
def test_get_current_user():
    headers = {"Authorization": f'Bearer {access}'}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "username" in data

# Тест удаления пользователя
def test_delete_user():
    headers = {"Authorization": f'Bearer {access}'}
    response = client.delete("/users/48", headers=headers)
    assert response.status_code == 200
    response = client.delete("/users/48", headers=headers)
    assert response.status_code == 404

# Тест обновления пользователя
def test_update_user():
    headers = {"Authorization": f'Bearer {access}'}
    response = client.put(
        "/users/1",
        headers=headers,
        json={"full_name": "newemail@mail.ru"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "newemail@mail.ru"


