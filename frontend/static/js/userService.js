// Получить пользователя
async function getUser() {
  try {
    const response = await fetch("/users/me");
    if (!response.ok) return null;
    return await response.json();
  } catch {
    return null;
  }
}

// Обновляет имя пользователя и аватар, если аватар не загружен пользователем, устанавливает стандарный.
export async function setupUser(imgElement, usernameElement) {
  const user = await getUser();
  const defaultAvatarLink =
    window.location.origin + "/avatars/default-avatar.png";

  if (user) {
    // Устанавливаем имя пользователя
    usernameElement.textContent = user.username;

    // Если у пользователя есть аватар в профиле — ставим его, иначе стандартный
    imgElement.src = user.avatar ? user.avatar : defaultAvatarLink;
  } else {
    // Если пользователь не авторизован, сбрасываем аватар на стандартный
    imgElement.src = defaultAvatarLink;
  }
}
