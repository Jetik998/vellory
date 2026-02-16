// logout.js
/**
 * Настраивает обработку кнопки выхода пользователя
 * @param {HTMLElement} logoutButton - кнопка выхода
 */
export function setupLogout(logoutButton) {
  if (!logoutButton) return;

  logoutButton.addEventListener("click", async () => {
    console.log("Кнопка выхода нажата"); // проверка
    try {
      const response = await fetch("/auth/logout", {
        method: "POST",
        credentials: "include",
      });

      if (response.ok) {
        window.location.reload(); // успешный выход → перезагрузка страницы
      } else {
        alert("Ошибка при выходе");
      }
    } catch (error) {
      console.error("Ошибка выхода:", error);
    }
  });
}
