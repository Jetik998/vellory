// Функция для автоматического обновления токена
async function refreshToken() {
  try {
    const response = await fetch("/auth/refresh", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
    });
    console.log(response);
    if (response.status === 200) {
      // Токен успешно обновлён, переходим на главную
      window.location.href = "/";
    }
  } catch (error) {
    console.error("Не удалось обновить токен", error);
  }
}

// Выполняем при загрузке страницы, ДО остального кода
refreshToken().catch(() => {});
