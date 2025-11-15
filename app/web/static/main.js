async function updateAvatar(imgElement) {
  try {
    const response = await fetch("users/avatar/get");
    if (!response.ok) return;

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);

    if (imgElement.src !== url) {
      imgElement.src = url;
    }
  } catch {
    // ошибки проглатываются намеренно
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  const logoutButton = document.getElementById("logoutButton");
  const userAvatar = document.getElementById("user-avatar-img");
  const fileInput = document.getElementById("fileInput");

  await updateAvatar(userAvatar);

  userAvatar.addEventListener("click", () => {
    fileInput.click();
  });

  fileInput.addEventListener("change", async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Предпросмотр
    const reader = new FileReader();
    reader.onload = (evt) => {
      userAvatar.src = evt.target.result;
    };
    reader.readAsDataURL(file);

    // Подготовка отправки
    const formData = new FormData();
    formData.append("file", file); // имя должно совпадать с параметром `file: UploadFile = File(...)`

    try {
      const response = await fetch("users/avatar/upload", {
        method: "POST",
        body: formData,
        credentials: "include",
      });

      // обработка ответа
      const data = await response.json();
      console.log(data);
    } catch (err) {
      console.error("Ошибка при загрузке аватара:", err);
    }
  });

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
