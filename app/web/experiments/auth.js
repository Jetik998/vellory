// Ожидаем полной загрузки DOM перед выполнением скрипта
document.addEventListener("DOMContentLoaded", function () {
  // Находим форму по ID
  const loginForm = document.getElementById("loginForm");

  // Добавляем обработчик события отправки формы
  if (loginForm) {
    loginForm.addEventListener("submit", async function (event) {
      // Предотвращаем стандартную отправку формы (перезагрузку страницы)
      event.preventDefault();

      // Собираем данные из формы
      const formData = new FormData(loginForm);
      const username = formData.get("username");
      const password = formData.get("password");

      // Создаем объект с данными для отправки
      const requestBody = new URLSearchParams();
      requestBody.append("username", username);
      requestBody.append("password", password);
      requestBody.append("grant_type", "password"); // обязательный параметр

      try {
        // Отправляем POST-запрос на сервер
        const response = await fetch("/api/auth/token", {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: requestBody,
        });

        // Проверяем статус ответа
        if (response.ok) {
          const data = await response.json();
          const accessToken = data.access_token;

          // Сохраняем токен в localStorage
          localStorage.setItem("access_token", accessToken);
          console.log("Токен успешно сохранен:", accessToken);

          // Переход на защищённую страницу
          fetch("/index", {
            headers: { Authorization: `Bearer ${accessToken}` },
          }).then(() => {
            window.location.href = "/index";
          });
        } else {
          const errorData = await response.json();
          console.error("Ошибка авторизации:", errorData);
          alert("Ошибка входа: " + (errorData.detail || "Неверные данные"));
        }
      } catch (error) {
        console.error("Сетевая ошибка:", error);
        alert("Ошибка соединения с сервером");
      }
    });
  }

  // Обработка выхода
  const logoutButton = document.getElementById("logoutButton");
  if (logoutButton) {
    logoutButton.addEventListener("click", async function () {
      console.log("Кнопка выхода нажата");
      try {
        const response = await fetch("/logout", {
          method: "POST",
          credentials: "include",
        });
        if (response.ok) {
          // localStorage.removeItem("access_token");
          window.location.href = "/";
        } else {
          alert("Ошибка при выходе");
        }
      } catch (error) {
        console.error("Ошибка выхода:", error);
      }
    });
  }
});
