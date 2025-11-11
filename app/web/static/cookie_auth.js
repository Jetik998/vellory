document.addEventListener("DOMContentLoaded", function () {
  const loginForm = document.getElementById("loginForm");
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const usernameInput = document.getElementById("username");
  const logoutButton = document.getElementById("logoutButton");
  const loginBtn = document.getElementById("loginBtn");
  const registerBtn = document.getElementById("registerBtn");
  const authBtnAction = document.getElementById("auth-btn-action");
  const highLight = document.getElementById("highlight");
  let mode = "login";

  // обработка формы входа
  if (loginForm) {
    loginForm.addEventListener("submit", async function (event) {
      event.preventDefault();
      if (mode === "login") {
        const requestBody = new URLSearchParams({
          email: emailInput.value,
          password: passwordInput.value,
        });

        try {
          const response = await fetch("/api/auth/token-cookie", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: requestBody,
            credentials: "include",
          });

          if (response.ok) {
            window.location.reload();
          } else {
            const errorData = await response.json();
            alert("Ошибка входа: " + (errorData.detail || "Неверные данные"));
          }
        } catch {
          alert("Ошибка соединения с сервером");
        }
      } else {
        const requestBody = {
          email: emailInput.value,
          username: usernameInput.value,
          password: passwordInput.value,
        };
        try {
          const response = await fetch("/api/auth/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(requestBody),
            credentials: "include",
          });
          if (response.ok) {
            loginForm.reset();
            authBtnAction.textContent = "Войти";
            setTimeout(() => {
              loginBtn.click();
            }, 1000);
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

    function updateUI() {
      if (mode === "register") {
        usernameInput.style.display = "block";
        highLight.style.left = "50%";
        authBtnAction.textContent = "Регистрация";
        document.querySelector("p").textContent = "Регистрация";
      } else {
        usernameInput.style.display = "none";
        highLight.style.left = "0";
        authBtnAction.textContent = "Войти";
        document.querySelector("p").textContent = "Войдите в свой аккаунт";
      }
    }

    registerBtn.addEventListener("click", () => {
      mode = "register";
      updateUI();
    });

    loginBtn.addEventListener("click", () => {
      mode = "login";
      updateUI();
    });

    // инициализация
    updateUI();

    // кнопка выхода
    if (logoutButton) {
      logoutButton.addEventListener("click", async function () {
        try {
          const response = await fetch("/logout", {
            method: "POST",
            credentials: "include",
          });

          if (response.ok) {
            window.location.reload();
          } else {
            alert("Ошибка при выходе");
          }
        } catch (error) {
          console.error("Ошибка выхода:", error);
        }
      });
    }
  }
});
