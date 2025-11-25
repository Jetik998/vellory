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
    window.location.origin + "/avatars/default-avatar.png";
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

  await updateUserData(userAvatar, usernameCaption);

  // Класс задачи
  class TaskCard {
    constructor() {
      // Находим шаблон карточки задачи на странице
      const template = document.querySelector(".task-container");

      // Уникальный идентификатор задачи
      this.id = getCurrentTaskId();
      // Приоритет задачи по умолчанию 0 (не установлен)
      this.taskPriority = 0;
      // Клонируем шаблон карточки, чтобы создать новую
      this.card = template.cloneNode(true);
      // Присваиваем уникальный id элементу карточки
      this.card.id = `task-${this.id}`;
      // Делаем карточку видимой (по умолчанию, возможно, скрыта в шаблоне)
      this.card.style.display = "flex";

      // Устанавливаем номер задачи на карточке
      this.setTaskNumber();
      // Настраиваем кнопку сохранения
      this.setupSaveButton();
      // Настраиваем кнопку отмены
      this.setupCancelButton();
      // Настраиваем обработку кликов по кругам приоритетов
      this.setupPriorityCircles();

      this.saveHandler = this.save.bind(this);
      this.cancelHandler = this.cancel.bind(this);
      this.priorityHandlers = []; // для кругов приоритета

      // Добавляем новую карточку в контейнер на странице
      document.querySelector(".person-boxes").appendChild(this.card);
    }

    // Метод для отображения номера задачи
    setTaskNumber() {
      const numberSpan = this.card.querySelector(".task-number");
      if (numberSpan) numberSpan.textContent = `#${this.id}`;
    }

    // Метод для настройки кнопки "Сохранить"
    setupSaveButton() {
      this.card
        .querySelector(".card-btn-save")
        .addEventListener("click", this.saveHandler);
    }
    setupCancelButton() {
      this.card
        .querySelector(".card-btn-cancel")
        .addEventListener("click", this.cancelHandler);
    }

    // Метод для настройки кликов по кругам приоритетов
    setupPriorityCircles() {
      const circles = this.card.querySelectorAll(".circle");
      circles.forEach((circle, index) => {
        const handler = () => this.togglePriority(circles, index); // сохраняем функцию в переменную
        circle.addEventListener("click", handler); // навешиваем обработчик
        this.priorityHandlers[index] = handler; // сохраняем ссылку для удаления
      });
    }

    // Метод для изменения приоритета задачи при клике на круг
    togglePriority(circles, index) {
      const circle = circles[index];
      const isActive = circle.classList.contains("active");

      // Если круг не активен, активируем все до выбранного включительно
      // Если уже активен, сбрасываем приоритет
      circles.forEach((c, i) => {
        if (!isActive && i <= index) {
          c.classList.remove("active"); // На всякий случай сбрасываем класс
          c.style.backgroundColor = c.dataset.color; // Устанавливаем цвет из data-атрибута
          circle.classList.add("active"); // Активируем выбранный круг
        } else {
          c.classList.remove("active"); // Деактивируем все остальные
          c.style.backgroundColor = "transparent"; // Сброс цвета
        }
      });

      // Сохраняем текущий уровень приоритета
      this.taskPriority = isActive ? 0 : index + 1;
      console.log(`Task #${this.id} priority:`, this.taskPriority);
    }

    // Метод для "сохранения" задачи
    save() {
      // Делаем все поля ввода и textarea неактивными
      this.card
        .querySelectorAll("input, textarea")
        .forEach((el) => (el.disabled = true));
      // Делаем круги приоритетов некликабельными
      this.card
        .querySelectorAll(".circle")
        .forEach((el) => (el.style.pointerEvents = "none"));
      // Деактивируем кнопку сохранения
      this.card
        .querySelectorAll(".card-btn")
        .forEach((btn) => (btn.style.display = "none"));
      // Увеличить счетчик
      incrementTaskId();
      // Cброса флага состояния создания задачи
      resetTaskFlag();
    }

    cancel() {
      // Удаляем карточку из DOM
      // 1. Снять все обработчики
      this.card
        .querySelector(".card-btn-save")
        ?.removeEventListener("click", this.saveHandler);
      this.card
        .querySelector(".card-btn-cancel")
        ?.removeEventListener("click", this.cancelHandler);
      this.card.querySelectorAll(".circle").forEach((circle, index) => {
        circle.removeEventListener("click", this.priorityHandlers[index]);
      });

      // 2. Удалить элемент из DOM
      this.card.remove();

      // 3. Обнулить ссылки
      this.card = null;
      this.saveHandler = null;
      this.cancelHandler = null;
      this.priorityHandlers = null;
      // Cброса флага состояния создания задачи
      resetTaskFlag();
    }
  }

  let taskCounter = 1;

  // Функция возвращает текущий последний ID без изменения счётчика
  function getCurrentTaskId() {
    return taskCounter;
  }

  // Функция увеличивает счётчик и возвращает новый ID
  function incrementTaskId() {
    return taskCounter++;
  }

  let createTaskButtonClicked = false;
  const createTaskBtn = document.getElementById("create-task");
  // Обработчик кнопки создания задач
  createTaskBtn.addEventListener("click", () => {
    if (!createTaskButtonClicked) {
      // Первый клик
      new TaskCard();
      createTaskButtonClicked = true; // включаем флаг
    } else {
      // Повторный клик — показываем уведомление
      alert("Завершите создание задачи или отмените.");
    }
  });
  // Пример сброса флага где-то в коде
  function resetTaskFlag() {
    createTaskButtonClicked = false;
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
