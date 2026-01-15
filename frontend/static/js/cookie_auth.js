document.addEventListener("DOMContentLoaded", function () {
  const loginForm = document.getElementById("loginForm");
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const usernameInput = document.getElementById("username");
  const loginBtn = document.getElementById("loginBtn");
  const registerBtn = document.getElementById("registerBtn");
  const authBtnAction = document.getElementById("auth-btn-action");
  const highLight = document.getElementById("highlight");
  let mode = "login";

  // Обработка формы входа и регистрации
  if (loginForm) {
    loginForm.addEventListener("submit", async function (event) {
      event.preventDefault();
      if (mode === "login") {
        const requestBody = {
          email: emailInput.value,
          password: passwordInput.value,
        };
        // === ВХОД ===
        try {
          const response = await fetch("/auth/authorize", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(requestBody),
            credentials: "include",
          });

          if (response.ok) {
            window.location.href = "/";
          } else {
            const errorData = await response.json();
            alert("Ошибка входа: " + (errorData.detail || "Неверные данные"));
          }
        } catch {
          alert("Ошибка соединения с сервером");
        }
        // === РЕГИСТРАЦИЯ ===
      } else {
        const requestBody = {
          email: emailInput.value,
          username: usernameInput.value,
          password: passwordInput.value,
        };

        // Отправка запроса на регистрацию
        try {
          const response = await fetch("/auth/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(requestBody),
            credentials: "include",
          });
          // Успешная регистрация → сброс формы и переключение в режим входа
          if (response.ok) {
            const originalColor = authBtnAction.style.backgroundColor;
            loginForm.reset();
            authBtnAction.style.backgroundColor = "green";
            authBtnAction.textContent = "Успешная Регистрация";
            setTimeout(() => {
              authBtnAction.style.backgroundColor = originalColor;
              loginBtn.click();
            }, 1500);
          } else if (response.status === 409) {
            const originalColor = authBtnAction.style.backgroundColor;
            const text = authBtnAction.textContent;
            authBtnAction.style.backgroundColor = "red";
            authBtnAction.textContent = "Имя или email уже занято";
            setTimeout(() => {
              authBtnAction.style.backgroundColor = originalColor;
              authBtnAction.textContent = text;
            }, 1500);
          } else {
            const errorData = await response.json();
            alert(
              "Ошибка регистрации: " + (errorData.detail || "Неверные данные"),
            );
          }
        } catch {
          alert("Ошибка соединения с сервером");
        }
      }
    });
    // === ИНТЕРФЕЙС СМЕНЫ РЕЖИМА РЕГИСТРАЦИЯ/ЛОГИН  ===
    function updateUI() {
      if (mode === "register") {
        usernameInput.style.display = "block";
        highLight.style.left = "50%";
        usernameInput.required = true;
        authBtnAction.textContent = "Регистрация";
        document.querySelector("p").textContent = "Регистрация";
      } else {
        usernameInput.style.display = "none";
        usernameInput.required = false;
        highLight.style.left = "0";
        authBtnAction.textContent = "Войти";
        document.querySelector("p").textContent = "Войдите в свой аккаунт";
      }
    }
    // === ПЕРЕКЛЮЧЕНИЕ РЕЖИМА РЕГИСТРАЦИЯ/ЛОГИН ===
    registerBtn.addEventListener("click", () => {
      mode = "register";
      updateUI();
    });

    loginBtn.addEventListener("click", () => {
      mode = "login";
      updateUI();
    });

    // === ИНИЦИАЛИЗАЦИЯ ИНТЕРФЕЙСА ===
    updateUI();
  }
});
