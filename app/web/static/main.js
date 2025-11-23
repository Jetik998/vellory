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
async function updateUserData(imgElement, usernameElement) {
  const user = await getUser();
  const defaultAvatarLink =
    "https://images.icon-icons.com/1378/PNG/512/avatardefault_92824.png";
  const baseAvatar = window.location.origin + "/avatars/background-avatar.png";
  console.log(imgElement.src);
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

document.addEventListener("DOMContentLoaded", async () => {
  const logoutButton = document.getElementById("logoutButton");
  const userAvatar = document.getElementById("user-avatar-img");
  const fileInput = document.getElementById("fileInput");
  const usernameCaption = document.getElementById("username-caption");
  const changeAvatar = document.getElementById("ChangeAvatar");
  const circles = document.querySelectorAll(".circle");

  await updateUserData(userAvatar, usernameCaption);

  let taskPriority = 0;

  circles.forEach((circle, index) => {
    circle.addEventListener("click", () => {
      // Проверяем, активен ли последний кликнутый круг
      const isActive = circle.classList.contains("active");

      circles.forEach((c, i) => {
        if (!isActive && i <= index) {
          c.classList.remove("active");
          c.style.backgroundColor = c.dataset.color;
          circle.classList.add("active");
        } else {
          c.classList.remove("active");
          c.style.backgroundColor = "transparent";
        }
      });
      taskPriority = isActive ? 0 : index + 1;
    });
  });

  // Функция для сброса всех кружков в прозрачные
  function resetCircles() {
    circles.forEach((circle) => {
      circle.style.backgroundColor = "transparent";
    });
    taskPriority = 0; // сброс приоритета
  }

  // При клике на элемент userAvatar программно «кликается» по fileInput.
  userAvatar.addEventListener("click", () => {
    fileInput.click();
  });

  // При клике на элемент userAvatar программно «кликается» по fileInput.
  changeAvatar.addEventListener("click", () => {
    fileInput.click();
  });

  fileInput.addEventListener("change", async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Предпросмотр аватара
    const reader = new FileReader();
    reader.onload = (evt) => {
      userAvatar.src = evt.target.result;
    };
    reader.readAsDataURL(file);

    // Подготовка отправки аватара
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
