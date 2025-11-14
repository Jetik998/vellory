document.addEventListener("DOMContentLoaded", function () {
  const logoutButton = document.getElementById("logoutButton");
  // === ОБРАБОТКА ВЫХОДА ===
  if (logoutButton) {
    logoutButton.addEventListener("click", async function () {
      console.log("Кнопка выхода нажата"); // проверка
      try {
        const response = await fetch("/logout", {
          method: "POST",
          credentials: "include",
        });
        // Успешный выход → обновление страницы
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
});
