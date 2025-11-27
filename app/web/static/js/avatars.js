// avatars.js

/**
 * Настраивает аватар пользователя: клик по картинке/кнопке и загрузка файла.
 * @param {HTMLElement} userAvatar - элемент img для аватара
 * @param {HTMLElement} changeAvatar - кнопка для смены аватара
 * @param {HTMLInputElement} fileInput - input type="file"
 */
export function setupAvatar(userAvatar, changeAvatar, fileInput) {
  if (!userAvatar || !changeAvatar || !fileInput) return;

  // Клик по аватару или кнопке вызывает input
  const triggerFileInput = () => fileInput.click();
  userAvatar.addEventListener("click", triggerFileInput);
  changeAvatar.addEventListener("click", triggerFileInput);

  // Обработка выбора файла
  fileInput.addEventListener("change", async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Предпросмотр аватара
    const reader = new FileReader();
    reader.onload = (evt) => {
      userAvatar.src = evt.target.result;
    };
    reader.readAsDataURL(file);

    // Подготовка отправки аватара на сервер
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("users/avatar/upload", {
        method: "POST",
        body: formData,
        credentials: "include",
      });

      const data = await response.json();
      console.log("Ответ сервера:", data);
    } catch (err) {
      console.error("Ошибка при загрузке аватара:", err);
    }
  });
}
