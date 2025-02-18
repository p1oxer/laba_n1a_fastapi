const apiBaseUrl = "http://localhost:8000";

let accessToken = "";
document.getElementById("login-form").addEventListener("submit", async function (event) {
    event.preventDefault(); // Остановка стандартного поведения формы

    const username = document.getElementById("username-login").value;
    const password = document.getElementById("password-login").value;

    const url = "http://127.0.0.1:8000/token";

    const headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    };

    const body = new URLSearchParams({
        grant_type: "password",
        username: username,
        password: password,
    });

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: headers,
            body: body,
        });

        const data = await response.json();
        console.log(data);

        if (data.access_token) {
            alert("Успешный вход! Токен: " + data.access_token);
            localStorage.setItem("token", data.access_token);
        } else {
            alert("Ошибка входа!");
        }
    } catch (error) {
        console.error("Ошибка запроса:", error);
        alert("Ошибка запроса!");
    }
});

async function getUserInfo() {
    if (!localStorage.getItem("token")) {
        document.getElementById("userInfo").textContent = "Сначала войдите в систему!";
        return;
    }
    const response = await fetch("http://localhost:8000/users/me", {
        method: "GET",
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    });

    const data = await response.json();
    for (const [key, value] of Object.entries(data)) {
        const li = document.createElement("li");
        li.textContent = `${key} - ${value}`;
        document.getElementById("userInfo").appendChild(li);
    }
    
    // document.getElementById("userInfo").textContent = JSON.stringify(data, null, 2);
}
document.getElementById("getMyInfo").addEventListener("click", getUserInfo);
async function fetchUsers() {
    if (!localStorage.getItem("token")) {
        document.getElementById("userInfo").textContent = "Сначала войдите в систему!";
        return;
    }
    // Выполняем GET-запрос к API для получения списка пользователей
    const response = await fetch(`${apiBaseUrl}/users/`, {
        method: "GET",
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    });
    // Преобразуем ответ в JSON-формат
    const users = await response.json();
    console.log(users);
    // Получаем элемент списка пользователей по его ID
    const userList = document.getElementById("user-list");
    // Очищаем текущий список пользователей
    userList.innerHTML = "";
    // Проходим по каждому пользователю и добавляем его в HTML-список
    users.forEach((user) => {
        const li = document.createElement("li");
        li.textContent = `${user.id}: ${user.username} (${user.email})`;
        userList.appendChild(li);
    });
}
document.getElementById("create-user-form").addEventListener("submit", async (e) => {
    // Предотвращаем стандартное поведение формы (перезагрузку страницы)
    e.preventDefault();
    // Получаем значения полей формы
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const full_name = document.getElementById("full_name").value;
    const password = document.getElementById("password").value;

    // Отправляем POST-запрос на сервер для создания нового пользователя
    const response = await fetch(`${apiBaseUrl}/register/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, email, full_name, password }),
    });

    // Проверяем успешность операции и показываем сообщение пользователю
    if (response.ok) {
        alert("User created successfully");
        // Обновляем список пользователей
        fetchUsers();
    } else {
        alert("Error creating user");
    }
});

document.getElementById("update-user-form").addEventListener("submit", async (e) => {
    // Предотвращаем стандартное поведение формы
    e.preventDefault();
    // Получаем значения полей формы
    const userId = document.getElementById("update-user-id").value;
    const username = document.getElementById("update-username").value;
    const email = document.getElementById("update-email").value;
    const full_name = document.getElementById("update-full_name").value;
    const password = document.getElementById("update-password").value;

    // Отправляем PUT-запрос на сервер для обновления данных пользователя
    const response = await fetch(`${apiBaseUrl}/users/${userId}`, {
        method: "PUT",
        headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
            "Content-Type": "application/json",
        },

        body: JSON.stringify({ username, email, full_name, password }),
    });

    // Проверяем успешность операции и показываем сообщение пользователю
    if (response.ok) {
        alert("User updated successfully");
        // Обновляем список пользователей
        fetchUsers();
    } else {
        alert("Error updating user");
    }
});

document.getElementById("delete-user-form").addEventListener("submit", async (e) => {
    // Предотвращаем стандартное поведение формы
    e.preventDefault();
    // Получаем ID пользователя для удаления
    const userId = document.getElementById("delete-user-id").value;

    // Отправляем DELETE-запрос на сервер для удаления пользователя
    const response = await fetch(`${apiBaseUrl}/users/${userId}`, {
        method: "DELETE",
        headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
            "Content-Type": "application/json",
        },
    });

    // Проверяем успешность операции и показываем сообщение пользователю
    if (response.ok) {
        alert("User deleted successfully");
        // Обновляем список пользователей
        fetchUsers();
    } else {
        alert("Error deleting user");
    }
});
// При загрузке страницы выполняем начальное получение списка пользователей
fetchUsers();
