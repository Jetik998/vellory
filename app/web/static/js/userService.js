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
  const baseAvatar = window.location.origin + "/avatars/background-avatar.png";
  if (user) {
    usernameElement.textContent = user.username;
    if (user.avatar && imgElement.src !== user.avatar) {
      imgElement.src = user.avatar;
    } else if (imgElement.src === baseAvatar) {
      imgElement.src = defaultAvatarLink;
    }
  } else {
    if (imgElement.src === baseAvatar) {
      imgElement.src = defaultAvatarLink;
    }
  }
}
